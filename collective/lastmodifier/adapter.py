from collective.lastmodifier.interfaces import ILastModifier
from Products.Archetypes.interfaces import IExtensibleMetadata
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.interface import implements


ANNOTATION_KEY = 'collective.lastmodifier'


class ATLastModifier(object):
    implements(ILastModifier)
    adapts(IExtensibleMetadata)

    def __init__(self, context):
        self.context = context

    def get(self):
        return (self._get_field().getAccessor(self.context)()
                or self.context.Creator())

    def set(self, userid, reindex=True):
        self._get_field().getMutator(self.context)(userid)
        if reindex:
            self.context.reindexObject(idxs=['last_modifier'])

    def _get_field(self):
        return self.context.Schema().getField('lastModifier')


class DXLastModifier(object):
    implements(ILastModifier)

    def __init__(self, context):
        self.context = context

    def get(self):
        return (IAnnotations(self.context).get(ANNOTATION_KEY, None)
                or self.context.Creator())

    def set(self, userid, reindex=True):
        IAnnotations(self.context)[ANNOTATION_KEY] = userid
        if reindex:
            self.context.reindexObject(idxs=['last_modifier'])
