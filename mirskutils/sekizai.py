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
    
    Usage::
    
        {% load mirskutils sekizai_tags %}
        <html>
          <head>
            <!-- an 'addtoblock' can be anywhere within a block/endblock -->
            <!-- all css files will be compacted together, including preprocessing of less -->
            {% addtoblock 'css' %}
              {% css 'css/app.css' %}
            {% endaddtoblock %}
            
            {% addtoblock 'js' %}
              {% js 'js/app.js' %}
            {% endaddtoblock %}
            
            
            {% render_block 'css' postprocessor 'mirskutils.sekizai.compress' %}
          </head>
          <body>
    
            <!-- if debug is True, javascript file <script> tags will be listed here --> 
            <!-- if debug is False, javascript files will be concatenated and compressed (cached) -->
            {% render_block 'js' postprocessor 'mirskutils.sekizai.compress' %}
          </body>
        </html>    
    '''
    
    return CompressorNode(nodelist=Template(data).nodelist, kind=name, mode='file').render(context=context)