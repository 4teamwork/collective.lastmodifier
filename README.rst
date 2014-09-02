Introduction
============

``collective.lastmodifier`` provides support for storing the user who made the
last modification on a content item. It extends Archetypes-based content types
with a `lastModifier` field using schemaextender. Further it registers an index
and a metadata column in `portal_catalog` and enables their usage in
collections.

Installation
============

Install ``collective.lastmodifier`` by adding it to the list of eggs in your
buildout or by adding it as a dependency of your policy package. Then run
buildout and restart your instance.

Go to Site Setup of your Plone site and activate the ``collective.lastmodifier``
add-on.


Last modifier adapter
=====================

In addition to the catalog index and metadata the last modifier
adapter provides easy access for getting the last modifier or for
setting it:

.. code:: python

    from collective.lastmodifier.interfaces import ILastModifier

    last_modifier = ILastModifier(context)
    last_modifier.get()  # returns the user id of the last modifier
    last_modifier.set(user_id)  # sets the last modifier


Compatibility
-------------

Runs with `Plone <http://www.plone.org/>`_ `4.1`, `4.2` and `4.3`.

It is currently only compatible with Archetypes, Dexterity is not compatible.


Links
=====

- Github project repository: https://github.com/4teamwork/collective.lastmodifier
- Issue tracker: https://github.com/4teamwork/collective.lastmodifier/issues
- Package on pypi: http://pypi.python.org/pypi/collective.lastmodifier
- Continuous integration: https://jenkins.4teamwork.ch/search?q=collective.lastmodifier


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``collective.lastmodifier`` is licensed under GNU General Public License, version 2.
