import functools
import logging


logger = logging.getLogger("deprecation")


def deprecated(author, date):
    """
        Function to mark code as suspected to be dead.
        If function is ever used, a warning will be logged to Sentry
        usage:

        @deprecated('your_name', '2015-03-27')
        def zombie_function(...):
    """
    def _decorator(f):
        @functools.wraps(f)
        def _wrapped(*args, **kwargs):
            logger.warn("Deprecated function called! {f_name} (deprecated by {author} on {date})"
                        .format(f_name=f.__name__, author=author, date=date), exc_info=True)
            return f(*args, **kwargs)
        return _wrapped
    return _decorator
