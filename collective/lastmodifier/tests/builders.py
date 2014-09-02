from ftw.builder import builder_registry
from ftw.builder.dexterity import DexterityBuilder


class DexterityTypeBuilder(DexterityBuilder):
    portal_type = 'DexterityType'


builder_registry.register('dexterity type', DexterityTypeBuilder)
