from setuptools import setup, find_packages
import os

version = '1.1.3'

tests_require = [
    'Products.CMFCore',
    'ftw.builder',
    'ftw.testing',
    'plone.app.dexterity',
    'plone.app.testing',
    'plone.directives.form',
    'unittest2',
    'zope.event',
    'zope.lifecycleevent',
    ]

setup(name='collective.lastmodifier',
      version=version,
      description="Extends Plone content with metadata about the last modifier",
      long_description=open("README.rst").read() + "\n" +
      open(os.path.join("docs", "HISTORY.txt")).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers

      classifiers=[
        "Framework :: Plone",
        'Framework :: Plone :: 4.3',
        "Programming Language :: Python",
        ],

      keywords='',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/collective.lastmodifier',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'Products.Archetypes',
        'Products.CMFCore',
        'Products.CMFPlone',
        'Products.GenericSetup',
        'archetypes.schemaextender',
        'collective.monkeypatcher',
        'ftw.profilehook',
        'plone.indexer',
        'setuptools',
        'zope.interface',
        ],

      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
