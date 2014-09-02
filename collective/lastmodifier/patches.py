from collective.lastmodifier.interfaces import ILastModifier
from Products.CMFCore.utils import getToolByName


def notifyModified(self):
    """Store the user id of the user that modified the object after calling
       the original method.
    """
    self._original_notifyModified()
    mtool = getToolByName(self, 'portal_membership', None)
    if mtool is None:
        return
    modifier = mtool.getAuthenticatedMember().getId()
    ILastModifier(self).set(modifier, reindex=False)


def applyPatch(scope, original, replacement):
    original_backup_name = '_original_' + original
    if getattr(scope, original_backup_name, None) is None:
        setattr(scope, original_backup_name, getattr(scope, original))
    setattr(scope, original, replacement)
