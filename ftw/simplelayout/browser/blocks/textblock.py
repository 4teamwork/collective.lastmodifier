from ftw.simplelayout.behaviors import ITeaser
from ftw.simplelayout.interfaces import IDisplaySettings
from zope.component import queryMultiAdapter
from zope.publisher.browser import BrowserView
import cssutils
import json


def parse_css(styles, attr, default=None):
    parsed = cssutils.parseStyle(styles)
    value = getattr(parsed, attr)
    if not value:
        return default

    value = value.rstrip('px')
    return value


class TextBlockView(BrowserView):

    def get_scaled_image(self):
        scale = self.context.restrictedTraverse('@@images')
        displaysettings = queryMultiAdapter((self.context, self.request),
                                            IDisplaySettings)
        styles = displaysettings.get_image_styles()

        # ridiculous large height, so it doesn't matters while scaling
        height = 10000

        if not styles:
            width = self.calculate_min_image_width()
            return scale.scale('image', width=width, height=height)
        else:
            width = int(parse_css(styles, 'width'))
            if parse_css(styles, 'height'):
                height = int(parse_css(styles, 'height'))
            return scale.scale('image', width=width, height=height)

    def get_style(self):
        displaysettings = queryMultiAdapter((self.context, self.request),
                                            IDisplaySettings)
        return displaysettings.get_image_styles()

    def img_tag(self):
        """Manually create image tag, because we set width and height width
        the style attribute to not break the columns in simplelayout.
        """
        scale = self.get_scaled_image()
        return ('<img src="{url}" alt="{title}" title="{title}" '
                'width="{width}" height="{height}" '
                'style="{style}" {additional}/>'.format(
                    **{'url': scale.url,
                       'title': self.context.Title(),
                       'width': scale.width,
                       'height': scale.height,
                       'style': self.get_style(),
                       'additional': self.additional()}))

    def additional(self):
        teaser_url = self.teaser_url()
        if teaser_url:
            return 'data-simplelayout-url="{0}"'.format(teaser_url)
        else:
            return ''

    def teaser_url(self):
        teaser = ITeaser(self.context)
        if not teaser:
            return None

        if teaser.internal_link:
            return teaser.internal_link.to_object.absolute_url()
        elif teaser.external_link:
            return teaser.external_link
        else:
            return None

    def get_simplelayout_view(self):
        contentpage = self.context.aq_parent
        return contentpage.restrictedTraverse(contentpage.getLayout())

    def calculate_min_image_width(self):
        view = self.get_simplelayout_view()
        settings = json.loads(view.load_default_settings())

        contentwidth = settings['contentwidth']
        images = settings['images']
        columns = settings['columns']
        margin_right = settings['margin_right']
        return contentwidth / columns / images - margin_right

    def get_image_wrapper_css_class(self):
        displaysettings = queryMultiAdapter((self.context, self.request),
                                            IDisplaySettings)
        styles = displaysettings.get_image_styles()

        direction = parse_css(styles, 'float', 'none')
        return 'sl-img-wrapper float-image-{0}'.format(direction)