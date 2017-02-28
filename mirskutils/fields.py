from jsonfield import JSONField
from django.core.exceptions import FieldError
import dpath.util
from .models import StructuredDictionary

from copy import deepcopy


class StructuredDictionaryField(JSONField):
    
    def __init__(self, structure={}, *args, **kwargs):
        if 'default' in kwargs:
            raise FieldError('please use the structure argument to provide default values')
        if kwargs.get('blank', False) or kwargs.get('null',False):
            raise FieldError('field only supports a structured response')
        self.structure = structure
        super(StructuredDictionaryField,self).__init__(*args, **kwargs)
        
    def pre_init(self, value, obj):
        d = super(StructuredDictionaryField, self).pre_init(value, obj)
        structure = deepcopy(self.structure)
        if d:
            return StructuredDictionary(structure, **d)
        return StructuredDictionary(structure, **structure)

try:
    from south.modelsinspector import add_introspection_rules
    _rules = []
    #_rules = [
        #(StructuredDictionaryField,),
        #[],
        #{
            #"structure":["structure", {"default":None} ]
        #}
    
    #]
    add_introspection_rules(_rules, ["^mirskutils\.fields\.(StructuredDictionaryField)"])
except ImportError:
    pass


