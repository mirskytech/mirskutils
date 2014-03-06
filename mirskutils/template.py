from django.template import Library as DjangoTemplateLibrary
from inspect import getargspec
from django.template.base import TagHelperNode, parse_bits

class Library(DjangoTemplateLibrary):

    #https://djangosnippets.org/snippets/1701/
    
    
    
    def withas_tag(self, func=None, takes_context=None, name=None):
        def dec(func):
            params, varargs, varkw, defaults = getargspec(func)
    
            class WithAsNode(TagHelperNode):
                def __init__(self, takes_context, args, kwargs, target_var=None):
                    super(WithAsNode, self).__init__(takes_context, args, kwargs)
                    self.target_var = target_var
    
                def render(self, context):
                    resolved_args, resolved_kwargs = self.get_resolved_arguments(context)
                    if self.target_var:
                        context[self.target_var] = func(*resolved_args, **resolved_kwargs)
                        return ''
                    return func(*resolved_args, **resolved_kwargs)
    
            function_name = (name or
                getattr(func, '_decorated_function', func).__name__)
    
            def compile_func(parser, token):
                bits = token.split_contents()[1:]
                
                target_var = None
                if len(bits) >=2 and bits[-2] == 'as':
                    target_var = bits[-1]
                    bits = bits[:-2]
                    
                args, kwargs = parse_bits(parser, bits, params,
                    varargs, varkw, defaults, takes_context, function_name)
                return WithAsNode(takes_context, args, kwargs, target_var)
    
            compile_func.__doc__ = func.__doc__
            self.tag(function_name, compile_func)
            return func
    
        if func is None:
            # @register.assignment_tag(...)
            return dec
        elif callable(func):
            # @register.assignment_tag
            return dec(func)
        else:
            raise TemplateSyntaxError("Invalid arguments provided to assignment_tag")