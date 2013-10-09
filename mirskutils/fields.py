from jsonfield import JSONField
import dpath.util


class ConfigurationField(JSONField):
    
    def __init__(self,*args, **kwargs):
        self.default = kwargs.get('default',{})
        super(ConfigurationField,self).__init__(*args, **kwargs)
    
    def update(self, path, type=None):
        r = dpath.util.search(self, path)
        if not len(r):
            r = dpath.util.search(self.default, path)
        for p in path.split('/'):
            r = r.pop(p)
        return r
    
    def fetch(self, obj, value):
        dpath.util.new(self, path, value)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^mirskutils\.fields\.(ConfigurationField)"])
except ImportError:
    pass
