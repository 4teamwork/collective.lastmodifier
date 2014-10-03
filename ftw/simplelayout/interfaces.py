# pylint: disable=E0211, E0213
# E0211: Method has no argument
# E0213: Method should have "self" as first argument

from ftw.simplelayout import _
from zope import schema
from zope.interface import Interface


class ISimplelayout(Interface):
    """Marker for Simplelayout content pages"""


class ISimplelayoutBlock(Interface):
    """Marker for simplelayout blocks"""


class ISimplelayoutView(Interface):
    """@@simplelayout-view view interface.
    """


class IBlockProperties(Interface):
    """Adapter for getting and setting information such as the current
    selected view for the block or the available views.
    """

    def __init__(context, request):
        """Adapts context and request.
        """

    def get_current_view_name():
        """Returns the name of the simplelayout view for displaying the
        context.
        """

    def get_available_views():
        """Returns a list of available views. Each element contains the
        viewname and a human readable title
        """

    def set_view(name):
        """Sets the current view of the context to ``name``.
        """


class IDisplaySettings(Interface):
    """Adapter for storing display settings on a blockish object.
    """

    def __init__(context, request):
        """Adapts context and request.
        """

    def set_position(position):
        """Sets the position of the object.

        Arguments:
        position -- dict with "top" and "left" keys.
        """

    def get_position():
        """Returns the stored position information as dict with "top" and
        "left".
        Returns ``None`` when nothing is stored.
        """

    def set_size(size):
        """Sets the size of the object.

        Arguments:
        size -- dict with "width" and "height" keys.
        """

    def get_size():
        """Returns the stored size information as dict with "width" and
        "height".
        Returns ``None`` when nothing is stored.
        """


class ISimplelayoutDefaultSettings(Interface):
    """Stores simplelayout default settings for the hole site"""

    columns = schema.Int(title=_(u'Amount of columns'),
                         default=4,
                         required=True)

    images = schema.Int(title=_(u'Amount of image columns'),
                        default=2,
                        required=True)

    contentwidth = schema.Int(title=_(u'Content width in pixel'),
                              default=960,
                              required=True)

    margin_right = schema.Int(title=_(u'margin between blocks in pixel'),
                              default=10,
                              required=True)

    contentarea = schema.TextLine(title=_(u'Content area selector'),
                                  description=(
                                  _(u'Danger: Change this only if you really '
                                    'know what you are doing')),
                                  default=u'#content',
                                  required=True)