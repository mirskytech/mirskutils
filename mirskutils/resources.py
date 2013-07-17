from tastypie.serializers import Serializer
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, Resource

from oauth2_provider.views import AuthorizationView, TokenView
from oauth2_provider.views.mixins import OAuthLibMixin

from django.conf.urls import patterns, url

from tastypie.exceptions import TastypieError, Unauthorized




class URLEncodeSerializer(Serializer):
    '''CanJS and other client-side frameworks send data with the urlencoded header
    even if the information is sent by POST. This adds that functionality.'''
    
    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'urlencode']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
        'urlencode': 'application/x-www-form-urlencoded',
        }
    def from_urlencode(self, data,options=None):
        """ handles basic formencoded url posts """
        qs = dict((k, v if len(v)>1 else v[0] )
            for k, v in urlparse.parse_qs(data).iteritems())
        return qs

    def to_urlencode(self,content): 
        pass    
    
class OAuth2Authorization(Authorization, OAuthLibMixin):
    
    def validate_user(self, request, *args, **kwargs):
        valid, r = self.verify_request(request)
        if not hasattr(request, 'user'):
            raise Unauthorized("You are not allowed to access that resource.")
        assert(request.user.is_authenticated())
        return valid
    
    def read_list(self, object_list, bundle):
        request = bundle.request
        valid, r = self.validate_user(request)
        if valid and hasattr(object_list.model, 'user'):
            return object_list.filter(user=request.user)
        return []
    
    def read_detail(self, object_list, bundle):        
        request = bundle.request
        valid, r = self.verify_user(request)
        if valid and bundle.obj and hasattr(bundle.obj, 'user'):
            return bundle.obj.individual == bundle.request.user
        return True
    
    def create_list(self, object_list, bundle):
        raise NotImplementedError('Cannot authorize all objects in a list.')
    
    def create_detail(self, object_list, bundle):
        return False
            
    def update_list(self, object_list, bundle):
        request = bundle.request
        valid, r = self.verify_request(request)

        if valid and hasattr(bundle.obj, 'user'):
            assert(request.user.is_authenticated())
            return [obj for obj in object_list if obj.user == request.user]
        return []

    def update_detail(self, object_list, bundle):
        request = bundle.request
        valid, r = self.verify_request(request)
        if valid and hasattr(bundle.obj, 'user'):
            return bundle.obj.user == request.user
        return False

    def delete_list(self, object_list, bundle):
        request = bundle.request
        valid, r = self.verify_request(request)

        if valid and hasattr(bundle.obj, 'user'):
            assert(request.user.is_authenticated())
            return [obj for obj in object_list if obj.user == request.user]
        return []

    def delete_detail(self, object_list, bundle):
        request = bundle.request
        valid, r = self.verify_request(request)
        if valid and hasattr(bundle.obj, 'user'):
            return bundle.obj.user == request.user
        return False
    
    
    
    
    
    
class GenericResource(ModelResource):
    
    class Meta:
        collection_name = 'data'
        serializer = URLEncodeSerializer()
        always_return_data = True
        authentication = SessionAuthentication()
        
        
class OAuth2Resource(Resource):
    
    def base_urls(self):
        return [
            url(r'^authorize/$', AuthorizationView.as_view(), name="authorize"),
            url(r'^token/$', TokenView.as_view(), name="token"),            
        ]
    
    
    class Meta:
        allowed_methods = ['get', 'post']
        resource_name = 'oauth'
        
        