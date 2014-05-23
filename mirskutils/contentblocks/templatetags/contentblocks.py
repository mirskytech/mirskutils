from mirskutils import template
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import ObjectDoesNotExist
from django.utils.safestring import mark_safe

register = template.Library()

#----------------------------------------------------------------------

@register.withas_tag
def contentblock(slug, field=None, category=None):
    """
        Description:
            Access a ContentBlock directly without rendering its contents
        
        Arugment(s):
            * ** slug  ** (required) : the unique identifier for the block
            * ** field ** : if specified, attribute provided
            * ** category ** : taxonomy to organize blocks
                
        Usage::
        
            {% contentblock 'contact-us' 'content' 'public' as ctnt %}
            {{ ctnt.text }}
    """
    
    d = { 'slug': slug.lower() }
    if category:
        d['category'] = ContentBlock.CATEGORY(category)
        
    try:
        cb = ContentBlock.objects.get(**d)
    except ObjectDoesNotExist:
        raise Http404("ContentBlock matching your query of '%s' does not exist" % slug)
    if field:
        return getattr(cb, field)
    return cb

@register.simple_tag
def contentblock_as_divs(slug, category=None):
    """
        Description:
            Render a ContentBlock wrapped in a ``<div>`` tag. For container blocks,
            each of its children are wrapped in a ``div``
        
        Arugment(s):
            * ** slug  ** (required) : the unique identifier for the block
            * ** category ** : taxonomy to organize blocks
                
        Usage::
        
            {% contentblock_as_divs 'landing-'|add:group 'content' 'public' %}
    """    
    
    d = { 'slug': slug.lower() }
    if category:
        d['category'] = ContentBlock.CATEGORY(category)
        
    try:
        cb = ContentBlock.objects.get(**d)
    except:
        raise Http404("ContentBlock matching your query of '%s' %s does not exist" % (slug.lower(),"in category '%s'" % category if category else ''))        
    
    cb = get_object_or_404(ContentBlock, **d)
    return cb.as_divs()

@register.withas_tag
def contentblock_exists(slug, category=None):
    """
        Description:
            Check to see if a ContentBlock exists and if it contains any content
        
        Arugment(s):
            * ** slug  ** (required) : the unique identifier for the block
            * ** category ** : taxonomy to organize blocks
                
        Usage::
        
            {% contentblock_exists 'contact-us' 'public' as ctnt_exists %}
            {% if ctnt_exists %}{% endif %}
    """    
    
    d = { 'slug': slug.lower() }
    if category:
        d['category'] = ContentBlock.CATEGORY(category)
        
    return ContentBlock.objects.filter(**d).exists() and not ContentBlock.objects.get(**d).is_empty()