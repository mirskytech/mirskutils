from functools import wraps, update_wrapper



'''from: http://djangosnippets.org/snippets/1701/'''

def with_as(f):
    """
    Decorator enabling a simple template tag to support "as my_var"
    syntax. When an as varible specified the result is added to the
    context under the variable name.

    example:
        @with_as
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
    
    
    
'''from: https://code.djangoproject.com/ticket/13879#no1'''
    
def method_decorator(decorator):
    """Converts a function decorator into a method decorator.
    
    This works properly for both: decorators with arguments and without them. The Django's version
    of this function just supports decorators with no arguments."""

    # For simple decorators, like @login_required, without arguments
    def _dec(func):
        def _wrapper(self, *args, **kwargs):
            def bound_func(*args2, **kwargs2):
                return func(self, *args2, **kwargs2)
            return decorator(bound_func)(*args, **kwargs)
        return wraps(func)(_wrapper)

    # Called everytime
    def _args(*argsx, **kwargsx):
        # Detect a simple decorator and call _dec for it
        if len(argsx) == 1 and callable(argsx[0]) and not kwargsx:
            return _dec(argsx[0])

        # Used for decorators with arguments, like @permission_required('something')
        def _dec2(func):
            def _wrapper(self, *args, **kwargs):
                def bound_func(*args2, **kwargs2):
                    return func(self, *args2, **kwargs2)
                return decorator(*argsx, **kwargsx)(bound_func)(*args, **kwargs)
            return wraps(func)(_wrapper)
        return _dec2

    update_wrapper(_args, decorator)
    # Change the name to aid debugging.
    _args.__name__ = 'method_decorator(%s)' % decorator.__name__
    return _args