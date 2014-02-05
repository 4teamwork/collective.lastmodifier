from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.testing import z2


class Fixture(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.lastmodifier
        self.loadZCML(package=collective.lastmodifier)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, "collective.lastmodifier:default")


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="Fixture:Integration")
