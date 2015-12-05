import dpath.util
from django.db import models
from jsonfield.fields import JSONField

class ConfigurationMixin(models.Model):
    
    initial = {}
    
    configuration = JSONField(default={})
        
    def get_option(self, path, default=None):
        r = dpath.util.search(self.configuration, path)
        if not len(r):
            r = dpath.util.search(self.initial, path)
        if not len(r):
            return default
        for p in path.split('/'):
            r = r.pop(p)
        return r if r else default
    
    def set_option(self, path, value):
        r = dpath.util.search(self.initial, path)
        for p in path.split('/'):
            if p not in r:
                raise KeyError('option %s not part of model configuration' % path)
            r = r.pop(p)
            
        str_types = [type(""), type(u'')]
        
        if type(r) in str_types:
            if not type(value) in str_types:
                raise TypeError('string option field should be %s, instead of %s' %(type(r),type(value)))
        elif type(r) is not type(value):
            raise TypeError("option field '%s' should be %s, instead of %s" % (path, type(r),type(value)))
        dpath.util.new(self.configuration, path, value)
        
    class Meta:
        abstract = True
        
        
class StructuredDictionary(dict):
    
    def __init__(self, structure=None, *args, **kwargs):
        self.structure = structure
        super(StructuredDictionary,self).__init__(*args, **kwargs)
    
    def get(self, path, default=None):
        r = dpath.util.search(dict(self.items()), path)
        if not len(r):
            r = dpath.util.search(self.structure, path)
        if not len(r):
            if default:
                return default
            raise KeyError("'%s' not part of field structure" % path)
        for p in path.split('/'):                    
            r = r.pop(p)
        if not r and default:
            return default
        return r
    
    def set(self, path, value):
        r = dpath.util.search(self.structure, path)
        for p in path.split('/'):
            if p not in r:
                raise KeyError("'%s' not part of field structure" % path)
            r = r.pop(p)
            
        if isinstance(r, unicode) or isinstance(r, str):
            if not isinstance(value, unicode) and not isinstance(value, str):
                raise TypeError("option field '%s' should be a str or unicode, instead of a(n) %s" % (path,type(value).__name__))
        elif type(r) is not type(value):
            raise TypeError("option field '%s' should be a(n) %s, instead of a(n) %s" % (path, type(r).__name__,type(value).__name__))
        dpath.util.new(self, path, value)
        
    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, value):
        if '/' not in key:
            return super(StructuredDictionary, self).__setitem__(key,value)
        return self.set(key, value)    
