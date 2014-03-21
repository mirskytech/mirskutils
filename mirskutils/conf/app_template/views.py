from django.views.generic import View
from mirskutils.views import LoginRequiredView
from django.shortcuts import render, redirect

"""
.. module:: useful_1
   :platform: Unix, Windows
   :synopsis: A useful module indeed.

.. moduleauthor:: Andrew Carter <andrew@invalid.com>


"""


class Home(View):
    """We use this as a public class example class.

    handles all kinds of request through :func:`dispatch` (inherited)

    .. note::

       An example of intersphinx is this: you **cannot** use :mod:`webapp.urls` on this class.

    """    
    
    def get(self, request):
        """respond to ajax request by rendering template
    
    
        Args:
        
            arg1 (str): argument one
            arg2 (bool): argument two
    
        Returns:
            < description of return >
            
            ``< example of return >``
            
        Raises:
            Exception: an exception that could be raised
        
        Usage:
        
        python : ``    ``
        
        javascript : ``
            $.post('/api/list', function(data) {
                console.log(data);
            });
        
        >> { 'html' : < rendered template>, 'status':'ok' }
        ``
        
        .. note::
           This only gets used when responding to a GET request
        
        """         
        return render(request, 'template/template.html', {})
        
        
        