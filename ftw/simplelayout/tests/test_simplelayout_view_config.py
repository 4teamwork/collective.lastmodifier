from ftw.builder import Builder
from ftw.builder import create
from ftw.simplelayout.testing import FTW_SIMPLELAYOUT_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from unittest2 import TestCase
import json


class TestSimpleayoutViewConfig(TestCase):

    layer = FTW_SIMPLELAYOUT_FUNCTIONAL_TESTING

    def setUp(self):
        self.cp = create(Builder('sl content page').titled(u'Content page'))
        self.view = self.cp.restrictedTraverse('@@simplelayout')

        self.expect = ('{"columns": 4, '
                       '"images": 2, '
                       '"contentwidth": 960, '
                       '"margin_right": 10, '
                       '"contentarea": "#content"}')

    def test_load_simplelayout_default_config_from_registry(self):

        self.assertEquals(self.expect, self.view.load_default_settings())

    def test_simplelayout_config_is_json_parsable(self):
        settings = json.loads(self.view.load_default_settings())
        self.assertTrue(isinstance(settings, dict),
                        'Simpleayout config is not is not json parsable.')

    @browsing
    def test_config_is_rendered_in_simplelayout_view(self, browser):
        browser.login().visit(self.cp, view='@@simplelayout')
        self.assertIn(
            self.expect,
            browser.css('.simplelayout').first.attrib[
                'data-simplelayout-config'],
            'The simeplayout config is not loaded correctly')

    def test_override_amound_of_columns_on_view(self):
        self.view.columns = 1
        settings = json.loads(self.view.load_default_settings())

        self.assertEquals(1, settings['columns'])
