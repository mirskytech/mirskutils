
- follow django's coding style
 
	https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/

	and the PEP-8 coding guidelines (http://www.python.org/dev/peps/pep-0008/), specifically:

	http://www.python.org/dev/peps/pep-0008/#id15
	http://www.python.org/dev/peps/pep-0008/#id17
	http://www.python.org/dev/peps/pep-0008/#id18
	
- follow google's javascript coding guidelines

	http://google-styleguide.googlecode.com/svn/trunk/javascriptguide.xml
	
- indentation for python code should be 4 spaces (not tabs)

- indentation for html and javascript code should be 2 spaces

- work should NEVER be done on the master branch, use 'git checkout -b myNewBranchName' ALWAYS

- changes required by the project should NEVER be done to installed packages

- all ``{% url 'view-name' %}`` should use ``{% load url from future %}``

- any new views created should use class-based view structure (https://docs.djangoproject.com/en/dev/topics/class-based-views/)

- all layout should be done using grid.css (blueprint css framework).

	- 4 column, customized layout grid for SportsCrunch design width/layout
	
	- more info: http://www.blueprintcss.org/
	
	- use span-1, span-2, etc and height-1, height-2, etc to specify all layout blocks

- By using the renderForm tag for form display, the forms should 'self' style with everything in form.css and button.css

- link buttons should use the following syntax

	``<a class="sc-button notyet" href="{% url 'foo' 'arg1' %}">``
		``<span class="sc-icon sc-icon-facebook"></span>``
		``<span class="sc-button-text">SIGN IN</span>``
	``</a>``
		
- form buttons should use the following syntax
		
	``<button type="submit" class="sc-button">Save</button>``	
		
- links that require an icon should use this syntax

    ``<a href="#"><span class="sc-icon sc-icon-feed"></span>My feed</a>``
	
	or if the icon is not yet available
	
	``<a href="#"><span class="sc-icon sc-icon-blank"></span>My feed</a>``

- series of items, such as links on menus or in navigation, should use ``<ul></ul>`` and not ``<div></div>``


