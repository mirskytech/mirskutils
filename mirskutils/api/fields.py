from tastypie.fields import ToOneField, ToManyField, NOT_PROVIDED



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
    
    