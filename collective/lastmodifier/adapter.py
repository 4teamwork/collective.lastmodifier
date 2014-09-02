from collective.lastmodifier.interfaces import ILastModifier
from Products.Archetypes.interfaces import IExtensibleMetadata
from zope.component import adapts
from zope.interface import implements


class ATLastModifier(object):
    implements(ILastModifier)
    adapts(IExtensibleMetadata)

    def __init__(self, context):
        self.context = context

    def get(self):
        return self._get_field().getAccessor(self.context)()

    def set(self, userid, reindex=True):
        self._get_field().getMutator(self.context)(userid)
        if reindex:
            self.context.reindexObject(idxs=['last_modifier'])

    def _get_field(self):
        return self.context.Schema().getField('lastModifier')
