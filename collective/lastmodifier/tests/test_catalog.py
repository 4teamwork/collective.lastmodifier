from Products.CMFCore.utils import getToolByName
from collective.lastmodifier.testing import LASTMODIFIER_INTEGRATION_TESTING
from ftw.builder import Builder
from ftw.builder import create
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
import unittest2


class TestCatalog(unittest2.TestCase):

    layer = LASTMODIFIER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.catalog = getToolByName(self.portal, 'portal_catalog')

    def test_index_is_registered(self):
        self.assertIn('last_modifier', self.catalog.indexes())

    def test_metadata_is_registered(self):
        self.assertIn('last_modifier', self.catalog.schema())

    def test_AT_index_and_metadata_is_updated_on_content_creation(self):
        hugo = create(Builder('user')
                      .named('Hugo', 'Boss')
                      .with_roles('Contributor'))
        login(self.portal, hugo.getId())

        folder = create(Builder('folder'))
        rid = self.catalog.getrid('/'.join(folder.getPhysicalPath()))

        self.assertDictContainsSubset(
            {'last_modifier': hugo.getId()},
            self.catalog.getIndexDataForRID(rid),
            'last_modifier index was not updated on content creation')

        self.assertDictContainsSubset(
            {'last_modifier': hugo.getId()},
            self.catalog.getMetadataForRID(rid),
            'last_modifier metadata was not updated on content creation')

    def test_AT_index_and_metadata_is_updated_on_content_modification(self):
        login(self.portal, TEST_USER_NAME)
        folder = create(Builder('folder'))

        john = create(Builder('user')
                      .named('John', 'Doe')
                      .with_roles('Contributor'))
        login(self.portal, john.getId())
        notify(ObjectModifiedEvent(folder))
        folder.reindexObject()

        rid = self.catalog.getrid('/'.join(folder.getPhysicalPath()))

        self.assertDictContainsSubset(
            {'last_modifier': john.getId()},
            self.catalog.getIndexDataForRID(rid),
            'last_modifier index was not updated on content modification')

        self.assertDictContainsSubset(
            {'last_modifier': john.getId()},
            self.catalog.getMetadataForRID(rid),
            'last_modifier metadata was not updated on content modification')
