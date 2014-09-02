from ftw.builder.testing import BUILDER_LAYER
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig
import collective.lastmodifier.tests.builders


class LastmodifierLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)

        import collective.lastmodifier.tests
        self.loadZCML(package=collective.lastmodifier.tests,
                      name='profiles.zcml')

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, "collective.lastmodifier:default")
        self.applyProfile(portal,
                          "collective.lastmodifier.tests:dxtype")

LASTMODIFIER_FIXTURE = LastmodifierLayer()
LASTMODIFIER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(LASTMODIFIER_FIXTURE,), name="collective.lastmodifier:Integration")
