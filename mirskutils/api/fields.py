from tastypie.fields import ToManyField, NOT_PROVIDED




class ToManySpecifyField(ToManyField):
    
    
    def __init__(self, to, attribute, null=True, blank=True, unique=False, help_text=None, fields=[]):
        
        self.fields = fields
        super(ToManySpecifyField, self).__init__(to, attribute, null=null, blank=blank, unique=unique, help_text=help_text)
        
        
    def dehydrate_related(self, bundle, related_resource, for_list=True):
        return { field:getattr(bundle.obj, field) for field in self.fields }