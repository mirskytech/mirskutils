.. SportsCrunch Platform

Web Application
=========================================

The SportsCrunch platform is actually several, separate applications:

.. image:: images/architecture.png

1. client-side application. html. css. javascript (primarily jquery & jquery ui)
2. cherokee web server. all traffic is encrypted using ssl.
3. static files. A mixture of pre-compiled/gathered and compiled-on-the-fly. Also, uploaded media.
4. uwsgi. python interpretter for web deployment.
5. solr. `apache lucene <http://lucene.apache.org/solr/>`_ search engine with index created and accessed using `haystack <http://haystacksearch.org/>`_.
6. django application(s). uses django's orm, views and templates. api for ajax requests built using `tastypie <http://tastypie.org>`_.
7. postgres. for storing relational data (users, teams, etc)
8. amazon s3. serving of all media (images, video).
9. rabbitmq. queuing system, accessed using the `celery <http://www.celeryproject.org>`_ libraries
10. 'crunchbot'. a set of asynchronous tasks that gather news stories and process playbook entries.
11. couchdb. no-sql storage for all playbook and newsfeed entries.

Concepts
--------------------------------------

A registered user's information is represented by an **Individual** and may have an affiliation with
an **Organization** as a member (player/coach) or as a follower (fan). While most professional teams are only associated
with a single sport, an **Organization** represents any institutional group, including high schools and colleges.
Therefore, the many-to-many relationship that defines a player/coach is described with a **Membership** which additionally
contains the sport, the years associated with a specific organization and their role (player or coach). An individual
can also be a follower of either another individual or an organization; These also are many-to-many using the
intermediate models of **Followship** and **Fan**, respectively.

A *playbook* is a collection of status updates, uploaded media (pictures/videos) or links to other websites; each item
is represented by an **Entry**. As a follower of an organization or individual, a user will see those entities' playbook
entries in their *feed*.

A professional player is allowed to sell items, or deals, on the site. These may be physical objects (jersey, sneakers, etc)
or access to another service or online resource. These are stored using ``cartridge.shop.models.Product`` and ``cartridge.shop.models.ProductVariant``
models. In order for a user to see (and then purchase) a deal, the individual has a **Subscription** to that player for a monthly
or annual fee.

.. note::
   An **Entry** is a non-relational document and subclasses from ``couchdb.mapping.Document``. All other classes are
   stored using Django's ORM and are derived from ``django.core.models.Model``.

.. image:: images/schema.png

1. **Individual** any user in the system -- amatuer or professional -- which can either be a registered
   user or a user created on behalf of individuals (usually professional). individuals are determined
   to be a professional if they have at least one affiliation with a professional organization. [#c1]_ 
2. **Organization** container for one or more teams. some organizations are limited by a single sport
   (eg Chicago Bulls) or membership can only be created (or changed) by an administrator. These are
   separately stored flags as there may be teams that are restricted to a sport, like lacrosse, that
   administrators don't need to have tight control over.
3. **Membership** many-to-many relationship associating player/coach to team.
4. **Followship** many-tomany relationship associating a user as a follower of another user.
5. **Fan** many-to-many relationship associating a user as a follower of an organization.
6. **Entry** a many-to-one ("foreign key") relationship. as these models are stored differently,
   an individual's username or an organization's slug is used to make the connection
   
.. rubric:: Footnotes

.. [#c1] some players have been loaded into the system who are not affiliated with a team as they
   are not currently playing on that team. there is a 'player_type' flag that will be deprecated once
   a team's roster can be differentiated by year.

Contents
------------------------------------------
.. toctree::
   :maxdepth 2
   
   Environment Setup <env>


.. toctree::
   :maxdepth: 2
   
   core/index
   registration
   crunchbot
   mobile
   deals
   subscription
   utils
   notifications
   


**Indices and tables**

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
