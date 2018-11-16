from Products.CMFCore.utils import getToolByName
from collective.lastmodifier.interfaces import ILastModifier


def set_last_modifier(context):
    mtool = getToolByName(context, 'portal_membership', None)
    if mtool is None:
        return
    modifier = mtool.getAuthenticatedMember().getId()

    last_modifier_manager = ILastModifier(context, None)
    if last_modifier_manager:
        last_modifier_manager.set(modifier)
