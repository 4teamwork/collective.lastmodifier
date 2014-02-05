from Products.CMFCore.utils import getToolByName
from collective.lastmodifier.testing import LASTMODIFIER_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
import unittest2 as unittest


class TestCatalog(unittest.TestCase):

    layer = LASTMODIFIER_INTEGRATION_TESTING

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
