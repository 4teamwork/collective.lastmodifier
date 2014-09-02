from collective.lastmodifier.interfaces import ILastModifier
from OFS.interfaces import IItem
from plone.indexer import indexer
from zope.component import queryAdapter


@indexer(IItem)
def last_modifier(obj, **kwargs):
    """An indexer which returns the userid of the person who modified the
       content.
    """
    last_modifier_adapter = queryAdapter(obj, ILastModifier)
    if last_modifier_adapter is None:
        return None

    return last_modifier_adapter.get() or obj.Creator()
