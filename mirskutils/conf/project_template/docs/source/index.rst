.. SportsCrunch Platform

SportsCrunch Platform's documentation
=========================================

There are two separate code bases for the SportsCrunch platform:


:doc:`webapp/index`
----------------------------------

Actually composed of several different applications, this is the part of the platform that handles 
the request / response flow for all http(s) traffic. This includes responding to user-initiated
browser, asynchronous ajax and mobile requests. Built using Django framework (version 1.5).

* :doc:`webapp/index`
* :doc:`webapp/env`


:doc:`mobileapp/index`
----------------------------------

'Native' applications, built using Apache Cordova (Phonegap). Currently, it runs as a lightweight,
ajax request-response wrapper around standard web application generated pages.

Documentation: `click here <mobileapp/indx>`_


Other Subdirectories
-----------------------------------

Other directories are legacy and can be removed in the future:

prelaunchapp
   used to gather email addresses prior to when the site was ready for primetime

data
   initial data (player information and photos) used to populate the site

design
   original html pages, inherited from previous owner. 

Table of Contents:

.. toctree::
   :maxdepth: 2
   
   Web Application <webapp/index>
   Mobile Application <mobileapp/index>
