mirskutils
==========

Utilities for django development


Modules
==========

models
---------------

Purpose : enumeration structure
Classes : Konstants, K
Functions : n/a
Usage :


```
from mirskutils.models import Konstants, K

KIND = Konstants(
    K(valueA=1, label="value a"),
    K(valueB=2, label="value b"),
    K(valueC=3, label="value c")
)

value = KIND.valueA

kind = forms.IntegerField(choices=KIND.choices())

def __unicode__(self):
    return "%s (%s)" % (self.name, KIND[self.kind])

```


sekizai
----------------

Purpose : compressor pipeline for use with sekizai_tags
Classes : n/a
Functions : compress
Usage :

```
{% load mirskutils sekizai_tags %}
<html>
    <head>
        {% addtoblock 'css' %}
          {% css 'css/app.css' %}
        {% endaddtoblock %}
    
        {% render_block 'css' postprocessor 'mirskutils.sekizai.compress' %}
    
    </head>
    <body>
    
    
    </body>
</html>
```

shortcuts
------------------

.. automodule:: shortcuts

views
__________________
.. automodule:: views




Template Tags
===============


mirskutils
---------------






Static
================















