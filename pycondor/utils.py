
import os
import subprocess
import time
import glob
import logging


# Specify logging settings
logging.basicConfig(
    format='%(levelname)s: pycondor - %(name)s : %(message)s')
logging_level_dict = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}


def _setup_logger(cls, verbose=0):
    """Configures and returns logger instance.

    This function takes a class instance (which must have a `name` attribute)
    and a verbosity level as parameters and returns a connfigured logger
    instance with the appropriate level set.

    Parameters
    ----------
    cls : object
        Class instance with attribute `name` (e.g. Dagman, Job)
    verbose: int
        Verbosity level. Values can be 0, 1, or 2, with 0 being the least
        verbose and 2 being the most verbose.

    Returns
    -------
    logger : logging.Logger
        Configured logger

    Allows classes to each have their own seperate loggers in order to
    allow for varying levels of verbosity. For example, you might want low
    verbosity for a pycondor Job, but high verbosity for a Dagman
    class. setup_logger() helps streamline this process.
    """
    if not hasattr(cls, 'name'):
        raise AttributeError('Input must have a "name" attribute.')
    # Set up logger
    if verbose not in logging_level_dict:
        raise KeyError('Verbose option {} for {} not valid. Valid options are {}.'.format(
            verbose, cls.name, logging_level_dict.keys()))
    logger = logging.getLogger(cls.name)
    logger.setLevel(logging_level_dict[verbose])

    return logger


def checkdir(path, makedirs):
    assert path is not None, 'path must be non-NoneType'
    outdir = os.path.dirname(path)
    if outdir == '':
        outdir = os.getcwd()
    if not os.path.isdir(outdir):
        if makedirs:
            print('The directory {} doesn\'t exist, '.format(outdir)
                  + 'creating it...')
            os.makedirs(outdir)
        else:
            raise OSError('The directory {} doesn\'t exist'.format(outdir))
    return


def get_queue(submitter=None):

    queue_command = 'condor_q'
    if submitter:
        queue_command += ' -submitter {}'.format(submitter)
    proc = subprocess.Popen([queue_command], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()

    return out


def string_rep(obj, quotes=False):
    '''Converts basic python objects to a string representation

    '''
    assert obj is not None, 'Input must not be None'

    quote = '"' if quotes else ''

    if isinstance(obj, (tuple, list)):
        obj_str = ', '.join([string_rep(item) for item in obj])
    else:
        obj_str = str(obj)

    return quote + obj_str + quote
