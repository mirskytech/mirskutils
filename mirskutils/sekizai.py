"""
Used to process all the js/css files gathered by sekizai through compression / preprocessing utilities utility. Leverages
django-compressor.

Sources:
    * https://gist.github.com/1311010
    
References:
    * https://github.com/ojii/django-sekizai/issues/4
    * https://github.com/jezdez/django_compressor.git
    * https://github.com/ojii/django-sekizai.git@0.6 or later
"""
from compressor.templatetags.compress import CompressorNode
from django.template.base import Template


def compress(context, data, name):
    '''
    pass static files through the {% compress <file type> %} template tag    
    
    
    Arguments:
    
    * **data**: the string from the template (the list of js or css files)

    * **name**: either 'js' or 'css' (the sekizai namespace)
    
    '''
    return CompressorNode(nodelist=Template(data).nodelist, kind=name, mode='file').render(context=context)