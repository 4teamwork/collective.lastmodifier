from ftw.builder.testing import BUILDER_LAYER
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer


class LastmodifierLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        import collective.lastmodifier
        self.loadZCML(package=collective.lastmodifier)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, "collective.lastmodifier:default")


LASTMODIFIER_FIXTURE = LastmodifierLayer()
LASTMODIFIER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(LASTMODIFIER_FIXTURE,), name="collective.lastmodifier:Integration")
