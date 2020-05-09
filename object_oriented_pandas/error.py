class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Exception):

    """
    Exception raised for errors in the input.

     Attributes:
         expr -- input in which the error occurred
         msg  -- explanation of the error
    """

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


