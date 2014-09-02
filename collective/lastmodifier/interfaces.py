from zope.interface import Interface


class ILastModifier(Interface):
    """Adapter for setting and retrieving the last modifier of
    an object.
    """

    def __init__(context):
        """Adapts an object.
        """

    def get():
        """Returns the ID of the last modifier.
        """

    def set(userid):
        """Sets the last modifier.
        """
