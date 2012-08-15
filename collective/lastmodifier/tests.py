import unittest2 as unittest
from collective.lastmodifier.testing import INTEGRATION_TESTING
from Products.CMFCore.utils import getToolByName
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import login


class TestLastModifier(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def test_creation(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])
        doc = portal[portal.invokeFactory('Document', 'doc')]
        last_modifier = doc.getField('lastModifier').getAccessor(doc)()
        self.assertEqual(last_modifier, TEST_USER_ID)

    def test_modification(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])
        doc = portal[portal.invokeFactory('Document', 'doc')]
        acl_users = getToolByName(portal, 'acl_users')
        acl_users.userFolderAddUser('modifier1', 'secret', ['Member'], [])
        setRoles(portal, 'modifier1', ['Editor'])
        login(portal, 'modifier1')
        doc.reindexObject() # "modify" the object
        last_modifier = doc.getField('lastModifier').getAccessor(doc)()
        self.assertEqual(last_modifier, 'modifier1')


class TestCatalog(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def test_index(self):
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        self.assertIn('last_modifier', catalog.indexes())
        self.assertIn('last_modifier', catalog.schema())

    def test_indexing(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])
        portal.invokeFactory('Document', 'doc')

        catalog = getToolByName(portal, 'portal_catalog')
        res = catalog(last_modifier='Nobody')
        self.assertEqual(len(res), 0)
        res = catalog(last_modifier=TEST_USER_ID)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].last_modifier, TEST_USER_ID)
