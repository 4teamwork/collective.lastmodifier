from collective.lastmodifier.interfaces import ILastModifier
from collective.lastmodifier.testing import LASTMODIFIER_INTEGRATION_TESTING
from ftw.builder import Builder
from ftw.builder import create
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase


class TestATLastModifierAdapter(TestCase):
    layer = LASTMODIFIER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.hugo = create(Builder('user')
                           .named('Hugo', 'Boss')
                           .with_roles('Contributor'))
        login(self.portal, self.hugo.getId())

    def test_getting_the_last_modifier(self):
        folder = create(Builder('folder'))
        self.assertEquals(self.hugo.getId(),
                          ILastModifier(folder).get())

    def test_setting_the_last_modifier_updates_the_catalog(self):
        folder = create(Builder('folder'))
        ILastModifier(folder).set('john.doe')
        self.assertEquals('john.doe',
                          ILastModifier(folder).get())

        rid = self.catalog.getrid('/'.join(folder.getPhysicalPath()))

        self.assertDictContainsSubset(
            {'last_modifier': 'john.doe'},
            self.catalog.getIndexDataForRID(rid),
            'last_modifier index was not updated on content creation')

        self.assertDictContainsSubset(
            {'last_modifier': 'john.doe'},
            self.catalog.getMetadataForRID(rid),
            'last_modifier metadata was not updated on content creation')
