from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.testing import z2


class LastmodifierLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.lastmodifier
        self.loadZCML(package=collective.lastmodifier)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, "collective.lastmodifier:default")


LASTMODIFIER_FIXTURE = LastmodifierLayer()
LASTMODIFIER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(LASTMODIFIER_FIXTURE,), name="collective.lastmodifier:Integration")
