from ftw.testing.layer import ComponentRegistryLayer
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import setRoles, TEST_USER_ID, TEST_USER_NAME, login
from plone.testing import z2
from plone.testing import zca
from zope.configuration import xmlconfig


class SimplelayoutZCMLLayer(ComponentRegistryLayer):
    """A layer which only sets up the zcml, but does not start a zope
    instance.
    """

    defaultBases = (zca.ZCML_DIRECTIVES,)

    def setUp(self):
        super(SimplelayoutZCMLLayer, self).setUp()

        import ftw.simplelayout.tests
        self.load_zcml_file('tests.zcml', ftw.simplelayout.tests)

SIMPLELAYOUT_ZCML_LAYER = SimplelayoutZCMLLayer()


class FtwSimplelayoutLayer(PloneSandboxLayer):

    def setUpZope(self, app, configurationContext):
        import ftw.simplelayout
        xmlconfig.file('configure.zcml', ftw.simplelayout,
                       context=configurationContext)

        z2.installProduct(app, 'ftw.simplelayout')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.simplelayout:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)


FTW_SIMPLELAYOUT_FIXTURE = FtwSimplelayoutLayer()
FTW_SIMPLELAYOUT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_SIMPLELAYOUT_FIXTURE,), name="FtwSimplelayout:Integration")
FTW_SIMPLELAYOUT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FTW_SIMPLELAYOUT_FIXTURE,), name='FtwSimplelayout:Functional')
