from Products.Archetypes.interfaces import IExtensibleMetadata
from plone.indexer import indexer


@indexer(IExtensibleMetadata)
def last_modifier(obj, **kwargs):
    """An indexer which returns the userid of the person who modified the
       content.
    """
    modifier = obj.getField('lastModifier').getAccessor(obj)()
    return modifier or obj.Creator()
