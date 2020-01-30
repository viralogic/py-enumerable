import warnings
import functools


def deprecated(reason):
    """
    This is a decorator which can be used to mark function as deprecated. It
    will result in a warning being emitted when the function is used.
    :param reason: a reason as a string
    :return: decorated function
    """

    def deprecated_decorator(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            warnings.simplefilter("always", DeprecationWarning)
            warnings.warn(
                u"{0} is deprecated. {1}".format(func.__name__, reason),
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return new_func

    return deprecated_decorator
