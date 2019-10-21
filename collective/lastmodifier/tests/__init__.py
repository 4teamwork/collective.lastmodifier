from ftw.testing import IS_PLONE_5
from unittest import TestCase

class LastModifierTestCase(TestCase):

    def flush_queue(self):
        if IS_PLONE_5:
            from Products.CMFCore.indexing import processQueue
            processQueue()
