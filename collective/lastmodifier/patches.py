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
    self.getField('lastModifier').getMutator(self)(modifier)


def applyPatch(scope, original, replacement):
    setattr(scope, '_original_' + original, getattr(scope, original))
    setattr(scope, original, replacement)
