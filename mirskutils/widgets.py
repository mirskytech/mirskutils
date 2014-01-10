from datetime import datetime

from django.forms import widgets
from django.template.loader import get_template
from django.template import Context
from django.forms.widgets import ClearableFileInput, CheckboxInput
from django.conf import settings
from django.template import Context, Template
from django.utils.safestring import mark_safe

from mirskutils.templatetags.mirskutils_img import srcThumbnail


class AutoCompleteSelect(widgets.Select):
    
    
    def render(self, name, value, attrs=None, choices=()):   
        
        t = get_template('autocompleteselect.html')
        
        d = {'name':name}
        
        if isinstance(self.choices, basestring):
            d.update({'source_url':self.choices})  
        else:
            d.update({'choices':self.choices})
        
        if value:
            if isinstance(self.choices, basestring):
                d.update({'value':value.pk, 'label':value.display_name()})
            else:
                _choices = dict([(str(c[0]),c[1]) for c in self.choices])
                if value in _choices:
                    d.update({'value':value, 'label':_choices[value]})
        
        return t.render(Context(d))
    
    class Media:
        css =  {
            'all':('lib/jqueryui/jquery-ui.custom.css',)
        }
        js = ('lib/jquery/jquery.min.js',
            'lib/jqueryui/jquery-ui.custom.min.js',)

class ImageFileInput(ClearableFileInput):
    
    def __init__(self, attrs=None):
        
        if attrs and ('width' in attrs or 'height' in attrs):
            self.width = attrs.get('width',0)        
            self.height = attrs.get('height',0)
        else:
            self.width = 0
            self.height = 75
        super(ImageFileInput,self).__init__(attrs)
    
    def render(self, name, value, attrs=None):
        
        context = {'name':name}

        if value and hasattr(value, 'url'):
            context['url'] = srcThumbnail(value.url, self.width, self.height)
            
        t = Template('''{% if url %}<img id="{{ name }}-img" src="{{ url }}">
        <div>
            <label for="{{ name }}-clear_id">Clear</label>     
            <input id="{{ name }}-clear_id" name="{{ name }}-clear" type="checkbox" />
        </div>
        {% endif %}
        <div style="margin-top:10px; padding:0px;">
            {% if url %}<label for="{{ name }}">Change</label>{% endif %}
            <input id="id_%(name)ss" name="{{ name }}" type="file" />
        </div>
        ''')
        
        return mark_safe(t.render(Context(context)))    