from collective.lastmodifier.interfaces import ILastModifier
from Products.CMFCore.utils import getToolByName


def set_last_modifier(context, event):
    mtool = getToolByName(context, 'portal_membership', None)
    if mtool is None:
        return
    modifier = mtool.getAuthenticatedMember().getId()
    ILastModifier(context).set(modifier)
