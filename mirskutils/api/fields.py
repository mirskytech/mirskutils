from tastypie.fields import ToOneField, ToManyField, NOT_PROVIDED

from tastypie.bundle import Bundle
from tastypie.exceptions import ApiFieldError, NotFound
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class ToManyPkField(ToManyField):
    
    def dehydrate_related(self, bundle, related_resource, for_list=True):
        '''
        Ignores full detail and full list and just returns the primary key
        '''        
        return bundle.obj.pk
    
class ToOnePkField(ToOneField):
    
    def dehydrate_related(self, bundle, related_resource, for_list=True):
        '''
        Ignores full detail and full list and just returns the primary key
        '''
        return bundle.obj.pk
    
class ToOneSpecifyField(ToOneField):
    
    def __init__(self, to, attribute, related_name=None, default=NOT_PROVIDED,
                 null=False, blank=False, readonly=False, help_text=None, fields=[]):
        
        self.fields = fields
        
        super(ToOneSpecifyField, self).__init__(
            to, attribute, related_name=related_name, default=default,
            null=null, blank=blank, readonly=readonly, help_text=help_text
        )
        
    def dehydrate_related(self, bundle, related_resource, for_list=True):
        
        return { getattr(bundle.obj, f) for f in self.fields }
    
class ToManySpecifyField(ToManyField):
    
    def __init__(self, to, attribute, related_name=None, default=NOT_PROVIDED,
                 null=False, blank=False, readonly=False, help_text=None, fields=[]):
        
        self.fields = fields
        
        super(ToManySpecifyField, self).__init__(
            to, attribute, related_name=related_name, default=default,
            null=null, blank=blank, readonly=readonly, help_text=help_text
        )
        
    def dehydrate_related(self, bundle, related_resource, for_list=True):
        
        return { f:getattr(bundle.obj, f) for f in self.fields }
    
    
class ToManyAuthorizedField(ToManyField):
    
    def dehydrate(self, bundle, for_list=True):
        if not bundle.obj or not bundle.obj.pk:
            if not self.null:
                raise ApiFieldError("The model '%r' does not have a primary key and can not be used in a ToMany context." % bundle.obj)

            return []

        the_m2ms = None
        previous_obj = bundle.obj
        attr = self.attribute

        if isinstance(self.attribute, basestring):
            attrs = self.attribute.split('__')
            the_m2ms = bundle.obj

            for attr in attrs:
                previous_obj = the_m2ms
                try:
                    the_m2ms = getattr(the_m2ms, attr, None)
                except ObjectDoesNotExist:
                    the_m2ms = None

                if not the_m2ms:
                    break

        elif callable(self.attribute):
            the_m2ms = self.attribute(bundle)

        if not the_m2ms:
            if not self.null:
                raise ApiFieldError("The model '%r' has an empty attribute '%s' and doesn't allow a null value." % (previous_obj, attr))

            return []

        self.m2m_resources = []
        m2m_dehydrated = []

        # TODO: Also model-specific and leaky. Relies on there being a
        #       ``Manager`` there.
        for m2m in the_m2ms.all():
            m2m_resource = self.get_related_resource(m2m)
            m2m_bundle = Bundle(obj=m2m, request=bundle.request)
            if m2m_resource._meta.authorization.read_detail(m2m, m2m_bundle):
                self.m2m_resources.append(m2m_resource)
                m2m_dehydrated.append(self.dehydrate_related(m2m_bundle, m2m_resource, for_list=for_list))

        return m2m_dehydrated    
