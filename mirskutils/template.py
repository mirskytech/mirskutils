from django.template import Library as DjangoTemplateLibrary
from inspect import getargspec
from django.template.library import TagHelperNode, parse_bits

from functools import wraps

# from https://djangosnippets.org/snippets/1701/

def with_as(f):
    """
    Decorator enabling a simple template tag to support "as my_var"
    syntax. When an as varible specified the result is added to the
    context under the variable name.

    example:
        @with_as
        @register.simple_tag
        def do_current_time(parser, token):
            ...
            return a_node

        {% current_time %}

        {% current_time as time %}
        {{ time }}
    """
    @wraps(f)
    def new_f(parser, token):
        contents = token.split_contents()

        if len(contents) < 3 or contents[-2] != 'as':
            return f(parser, token)

        as_var = contents[-1]
        # Remove 'as var_name' part from token
        token.contents =  ' '.join(contents[:-2])
        node = f(parser, token)
        patch_node(node, as_var)
        return node
    return new_f

def patch_node(node, as_var):
    """
    Patch the render method of node to silently update the context.
    """
    node._old_render = node.render

    # We patch a bound method, so self is not required
    @wraps(node._old_render)
    def new_render(context):
        context[as_var] = node._old_render(context)
        return ''
    
    node.render = new_render
