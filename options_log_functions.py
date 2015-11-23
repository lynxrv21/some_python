# --*--codding:utf-8--*--

"""options parser, config and logger setting functions."""

import ConfigParser
import logging
import logging.config
import os

from optparse import OptionParser


def set_options():
    """Create parser to process command line options, returns a dictionary.

    :Return:
        dictionary with parsed options.
    """
    parser = OptionParser(usage='%prog [options]')
    # defining required options
    parser.add_option('-v', '--verbose', action='store_true', default=False,
                      help='print info and warning messages [default: %default]'
                           ' log will include only critical and error messages'
                           ' by default')
    # parser.add_option('-v', '--verbose', help="verbosity level (0..2)",
    #                   choices=['0', '1', '2'])
    parser.add_option('-o', '--operation',
                      help="choose operation to perform: 'add', 'edit',"
                           " 'delete', 'retrieve'",
                      choices=['add', 'edit', 'delete', 'retrieve'])
    parser.add_option('-f', '--flag', help='flag value')

    (options, args) = parser.parse_args()
    if options.operation is None:
        parser.print_usage()
        parser.exit('Please, choose operation.')
    else:
        return options

def set_config(options, verbosity=0, database=None):
    """Read configuration options from file, merge them with command line
    options.

    :Parameters:
        - 'options': command line options.
        - 'verbosity': verbosity level, int.
        - 'database': output database name.

    :Return:
        - 'verbosity': verbosity level, int.
        - 'database': output database name, string.
    """
    try:
        if options.config:
            config = ConfigParser.ConfigParser()
            config.read(options.config)
            verbosity = config.get('task1', 'verbosity')
            database = config.get('base', 'database')

        if options.verbose:
            verbosity = int(options.verbose)
        if options.database:
            database = options.database

        return verbosity, database

    except (ConfigParser.Error, Exception) as err:
        raise MyError('Configuration error: %s' % err)

def set_log(verbose, logfile='log.ini', logger_name=None):
    """Create logger, set logging level, read settings from config file.

    :Parameters:
        - 'verbose': boolean.
        - 'logfile': logger configuration file name in current folder, e.g.
                     'log.conf'.

    :Return:
        logger object.
    """
    try:
        dirname = os.getcwd()
        log_path = os.path.join(dirname, logfile)
        try:
            # set up logging
            logging.config.fileConfig(log_path)
            # create Logger
            logger = logging.getLogger(logger_name)
            # setting the logging level due to verbose argument
            levels = {0: logging.CRITICAL, 1: logging.WARNING, 2: logging.DEBUG}
            level = levels.get(verbose)
            logger.setLevel(level)
            return logger
        except (ConfigParser.Error, Exception) as err:
            raise MyError(
                'Configuration error, check %s: %s' % (log_path, err,))
    except (OSError, IOError) as err:
        raise MyError('Env error: %s' % (err,))
