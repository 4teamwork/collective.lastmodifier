from Acquisition import aq_inner
from ftw.simplelayout.interfaces import IPageConfiguration
from ftw.simplelayout.interfaces import ISimplelayoutContainerConfig
from ftw.simplelayout.interfaces import ISimplelayoutDefaultSettings
from ftw.simplelayout.utils import get_block_html
from ftw.simplelayout.utils import normalize_portal_type
from plone import api
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ZODB.POSException import ConflictError
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.contentprovider.interfaces import ITALESProviderExpression
from zope.interface import implements
from zope.tales import expressions
import json
import logging
import re


LOG = logging.getLogger('ftw.simplelayout')


class CleanedViewPageTemplateFile(ViewPageTemplateFile):
    """Remove spaces and newlines between tags - This allows us to use
    'empty' selector in css.
    """

    def _prepare_html(self, text):
        text, type_ = super(ViewPageTemplateFile, self)._prepare_html(text)
        return re.sub(">\s*<", "><", text), type_


class BaseSimplelayoutExpression(object):

    fallbackview = ViewPageTemplateFile('templates/render_block_error.pt')
    structure = CleanedViewPageTemplateFile('templates/structure.pt')

    @property
    def one_layout_one_column(self):
        return [{"cols": [{"blocks": []}]}]

    def rows(self):
        """ Return datastructure for rendering blocks.
        """
        page_conf = IPageConfiguration(self.context)
        blocks = self._blocks()

        rows = page_conf.load().get(self.name, self.one_layout_one_column)

        for row in rows:
            row['class'] = 'sl-layout'
            for col in row['cols']:
                col['class'] = 'sl-column sl-col-{}'.format(len(row['cols']))
                col['blocks'] = filter(
                    lambda block: block.get('uid', '') in blocks,
                    col['blocks'])

                for block in col['blocks']:
                    obj = blocks[block['uid']]
                    block['obj_html'] = self._render_block_html(obj)
                    block['type'] = normalize_portal_type(obj.portal_type)
                    block['url'] = obj.absolute_url()
                    block['id'] = obj.getId()

        # Append blocks, which are not in the simplelayout configuration into
        # the last column.

        if self.name == 'default':
            for uid, obj in self._blocks_without_state():
                rows[-1]['cols'][-1]['blocks'].append(
                    {
                        'uid': uid,
                        'obj_html': self._render_block_html(obj),
                        'type': normalize_portal_type(obj.portal_type),
                        'url': obj.absolute_url(),
                        'id': obj.getId(),
                    }
                )

        return rows

    def _get_first_column_config(self):
        settings = self._get_sl_settings()
        if settings and settings.get('layout'):
            return self._get_sl_settings()['layout'][0]
        else:
            # One column by default.
            return 1

    def _render_block_html(self, block):

        try:
            html = get_block_html(block)
        except ConflictError:
            raise
        except Exception, exc:
            html = self.fallbackview()
            LOG.error('Could not render block: {}: {}'.format(
                exc.__class__.__name__,
                str(exc)))

        return html

    def _blocks(self):
        """ Return block objects by UID.
        """

        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        blocks = catalog(
            object_provides="ftw.simplelayout.interfaces.ISimplelayoutBlock",
            path={'query': '/'.join(context.getPhysicalPath()), 'depth': 1},
        )
        return {block.UID: block.getObject() for block in blocks}

    def _blocks_without_state(self):
        page_conf = IPageConfiguration(self.context)
        saved_blocks = []

        for container in page_conf.load().values():
            for row in container:
                for col in row['cols']:
                    for block in col['blocks']:
                        if 'uid' in block:
                            saved_blocks.append(block['uid'])

        return filter(lambda x: x[0] not in saved_blocks,
                      self._blocks().items())

    def _get_sl_settings(self):
        # 1. global settings
        registry = getUtility(IRegistry)
        settings = json.loads(
            registry.forInterface(ISimplelayoutDefaultSettings).slconfig)

        # 2. Update with Permission check
        self.update_permission_related_settings(settings)

        # 3. Update with ISimplelayoutContainerConfig adapter
        adapter = queryMultiAdapter((self.context, self.request),
                                    ISimplelayoutContainerConfig)
        if adapter is not None:
            adapter(settings)

        # 4. View level customizations
        method = 'update_simplelayout_settings'
        if method in dir(self.view) and callable(getattr(self.view, method)):
            getattr(self.view, method)(settings)
        return settings

    def get_simplelayout_settings(self):
        return json.dumps(self._get_sl_settings())

    def update_permission_related_settings(self, settings):
        settings['canChangeLayouts'] = api.user.has_permission(
            'ftw.simplelayout: Change Layouts',
            obj=self.context)
        settings['canEdit'] = api.user.has_permission(
            'Modify portal content',
            obj=self.context)


class SimplelayoutExpression(BaseSimplelayoutExpression,
                             expressions.StringExpr):
    """Simplelayout tales expression
    Usage: <div tal:content='structure simplelayout: default' /> """

    implements(ITALESProviderExpression)

    def __call__(self, econtext):
        self.name = super(SimplelayoutExpression, self).__call__(econtext)
        self.context = econtext.vars['context']
        self.request = econtext.vars['request']
        self.view = econtext.vars['view']

        return self.structure()


try:
    from chameleon.astutil import Symbol
    from chameleon.tales import StringExpr
    from z3c.pt.expressions import ContextExpressionMixin
except ImportError:
    pass
else:
    def render_simplelayout_expression(econtext, name):
        renderer = BaseSimplelayoutExpression()
        renderer.name = name.strip()
        renderer.context = econtext.get('context')
        renderer.request = econtext.get('request')
        renderer.view = econtext.get('view')
        return renderer.structure()

    class ChameleonSimplelayoutExpression(ContextExpressionMixin, StringExpr):
        transform = Symbol(render_simplelayout_expression)
