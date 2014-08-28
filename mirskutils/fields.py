from jsonfield import JSONField
from django.core.exceptions import FieldError
import dpath.util


class StructuredDictionaryField(JSONField):
    
    def __init__(self, structure, *args, **kwargs):
        if 'default' in kwargs:
            raise FieldError('please use the structure argument to provide default values')
        if kwargs.get('blank', False) or kwargs.get('null',False):
            raise FieldError('field only supports a structured response')
        self.structure = kwargs.pop('structure',{})
        super(StructuredDictionaryField,self).__init__(*args, **kwargs)
    
    def get(self, path, **kwargs):
        r = dpath.util.search(self, path)
        if not len(r):
            r = dpath.util.search(self.structure, path)
        if not len(r):
            if hasattr(kwargs, 'default'):
                return kwargs.get('default')
            raise KeyError("'%s' not part of field structure" % path)
        for p in path.split('/'):                    
            r = r.pop(p)
        if not r and hasattr(kwargs, 'default'):
            return kwargs.get('default')
        return r
    
    def set(self, path, value):
        dpath.util.search(self, path)
        for p in path.split('/'):
            if p not in r:
                raise KeyError("'%s' not part of field structure" % path)
            r = r.pop(p)
            
        if isinstance(r, unicode) or isinstance(r, str):
            if not isintance(value, unicode) and not isinstance(value, str):
                raise TypeError('option field should be string, instead of %s' % type(value))
        elif type(r) is not type(value):
            raise TypeError("option field '%s' should be %s, instead of %s" % (path, type(r),type(value)))
        dpath.util.new(self.configuration, path, value)
        
    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, value):
        return self.set(key, value)
        

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^mirskutils\.fields\.(StructuredDictionaryField)"])
except ImportError:
    pass


