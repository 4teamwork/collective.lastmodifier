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


class TestArchetypesField(unittest2.TestCase):

    layer = LASTMODIFIER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_field_lastmodifier_field_is_available(self):
        login(self.portal, TEST_USER_NAME)
        folder = create(Builder('folder'))
        self.assertIn('lastModifier', folder.Schema().keys())

    def test_modifier_is_set_on_creation(self):
        hugo = create(Builder('user')
                      .named('Hugo', 'Boss')
                      .with_roles('Contributor'))
        login(self.portal, hugo.getId())

        folder = create(Builder('folder'))
        self.assertEquals(hugo.getId(),
                          folder.getField('lastModifier').get(folder))

    def test_modifier_is_updated_on_modification(self):
        hugo = create(Builder('user')
                      .named('Hugo', 'Boss')
                      .with_roles('Contributor'))
        login(self.portal, hugo.getId())
        folder = create(Builder('folder'))

        john = create(Builder('user')
                      .named('John', 'Doe')
                      .with_roles('Editor', on=folder))
        login(self.portal, john.getId())
        notify(ObjectModifiedEvent(folder))
        folder.reindexObject()

        self.assertEquals(john.getId(),
                          folder.getField('lastModifier').get(folder))
