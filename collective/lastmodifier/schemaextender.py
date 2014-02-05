from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from Products.Archetypes import atapi
from Products.CMFPlone import PloneMessageFactory as _
from zope.interface import implements


class ExtensionStringField(ExtensionField, atapi.StringField):
    """A string field for extending schemas."""


class LastModifierExtender(object):
    implements(ISchemaExtender)

    fields = [
        ExtensionStringField(
            'lastModifier',
            schemata='ownership',
            widget=atapi.StringWidget(
                label=_(u'label_last_modifier', default=u'Last modified by'),
                description=_(u'help_last_modifier',
                              default=u'The user who made the last '
                                       'modification on this content.'),
                visible={'edit': 'invisible', 'view': 'invisible'},
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
