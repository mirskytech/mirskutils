from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, Resource, ResourceOptions, ModelDeclarativeMetaclass

#from oauth2_provider.views import AuthorizationView, TokenView
#from oauth2_provider.views.mixins import OAuthLibMixin

from django.conf.urls import patterns, url

from tastypie.exceptions import TastypieError, Unauthorized

from serializers import URLEncodeSerializer
    
#class OAuth2Authorization(Authorization, OAuthLibMixin):
    
    #def validate_user(self, request, *args, **kwargs):
        #valid, r = self.verify_request(request)
        #if not hasattr(request, 'user'):
            #raise Unauthorized("You are not allowed to access that resource.")
        #assert(request.user.is_authenticated())
        #return valid
    
    #def read_list(self, object_list, bundle):
        #request = bundle.request
        #valid, r = self.validate_user(request)
        #if valid and hasattr(object_list.model, 'user'):
            #return object_list.filter(user=request.user)
        #return []
    
    #def read_detail(self, object_list, bundle):        
        #request = bundle.request
        #valid, r = self.verify_user(request)
        #if valid and bundle.obj and hasattr(bundle.obj, 'user'):
            #return bundle.obj.individual == bundle.request.user
        #return True
    
    #def create_list(self, object_list, bundle):
        #raise NotImplementedError('Cannot authorize all objects in a list.')
    
    #def create_detail(self, object_list, bundle):
        #return False
            
    #def update_list(self, object_list, bundle):
        #request = bundle.request
        #valid, r = self.verify_request(request)

        #if valid and hasattr(bundle.obj, 'user'):
            #assert(request.user.is_authenticated())
            #return [obj for obj in object_list if obj.user == request.user]
        #return []

    #def update_detail(self, object_list, bundle):
        #request = bundle.request
        #valid, r = self.verify_request(request)
        #if valid and hasattr(bundle.obj, 'user'):
            #return bundle.obj.user == request.user
        #return False

    #def delete_list(self, object_list, bundle):
        #request = bundle.request
        #valid, r = self.verify_request(request)

        #if valid and hasattr(bundle.obj, 'user'):
            #assert(request.user.is_authenticated())
            #return [obj for obj in object_list if obj.user == request.user]
        #return []

    #def delete_detail(self, object_list, bundle):
        #request = bundle.request
        #valid, r = self.verify_request(request)
        #if valid and hasattr(bundle.obj, 'user'):
            #return bundle.obj.user == request.user
        #return False
    

class GenericOptions(ResourceOptions):
    collection_name = 'data'
 
    
class GenericDeclarativeMetaclass(ModelDeclarativeMetaclass):
    
    def __new__(cls, name, bases, attrs):
        new_class = super(GenericDeclarativeMetaclass,cls).__new__(cls, name, bases, attrs)
        new_class._meta.collection_name = 'data'
        new_class._meta.serializer = URLEncodeSerializer()
        new_class._meta.always_return_data = True
        new_class._meta.authentication = SessionAuthentication()           
        return new_class    
    
class GenericResource(ModelResource):
    
    __metaclass__ = GenericDeclarativeMetaclass
    
    def obj_create(self, bundle, **kwargs):

        if hasattr(bundle.obj.__class__,'user') and bundle.request:
            return super(GenericResource,self).obj_create(bundle, user=bundle.request.user)
            
        return super(GenericResource,self).obj_create(bundle)
        
        
#class OAuth2Resource(Resource):
    
    #def base_urls(self):
        #return [
            #url(r'^authorize/$', AuthorizationView.as_view(), name="authorize"),
            #url(r'^token/$', TokenView.as_view(), name="token"),            
        #]
    
    
    #class Meta:
        #allowed_methods = ['get', 'post']
        #resource_name = 'oauth'
        
        