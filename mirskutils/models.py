class K:
    def __init__(self, label=None, **kwargs):
        assert(len(kwargs) == 1)
        for k, v in kwargs.items():
            self.id = k
            self.v = v
        self.label = label or self.id

class Konstants:
    def __init__(self, *args):
        self.klist = args
        for k in self.klist:
            setattr(self, k.id, k.v)

    def choices(self):
        return [(k.v, k.label) for k in self.klist]
    
    def active_choices(self):
        return [(k.v, k.label) for k in self.klist if k.v > -1 ]
    
    def keysandlabels(self):
        return [(k.v, k.id) for k in self.klist]    
    
    def labels(self):
        return [k.label for k in self.klist]
    
    def key(self, v):
        for ks in self.klist:
            if v==ks.v: return ks.id
        return None

    def display(self, k):
        for ks in self.klist:
            if k==ks.v: return ks.label
        return ""

    def __getitem__(self,k):
        return self.display(int(k))
    
    def __call__(self, l):
        for ks in self.klist:
            if l.lower()==ks.label.lower() or l.lower() == ks.id.lower(): return ks.v
        return None
    
    def append(self, k):
        setattr(self, k.id, k.v)

import dpath.util
from django.db import models

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
                raise KeyError('option %s not part of model configuraiton' % path)
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