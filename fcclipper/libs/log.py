""" Logging Module """
import logging
from rich.logging import RichHandler

def setup_richlogging(level=logging.DEBUG):
    """ Setup logging to go to stderr.  """

    fmt = '%(message)s'
    #datefmt = '%m-%d %H:%M:%s'
    datefmt = '%m-%d %H:%M:%S'

    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    handler=RichHandler(markup=True)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(level)


def module_logger(mod_name):
    """ Create a logger to be used globally within a module. """

    mod_parts = mod_name.split('.')
    if len(mod_parts) > 1:
        mod_name = mod_parts[-1]

    return logging.getLogger(mod_name)
