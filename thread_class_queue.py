#!/usr/bin/python
# --*--codding:utf-8--*--

"""Module parses given url address, writes found URLs to database."""

import logging
import logging.config
import Queue
import re
import socket
import threading
import time
import urllib2

from bs4 import BeautifulSoup


class MyError(Exception):
    pass


URL_PATTERN = r'((http(s?))\:\/\/)((www.|[a-zA-Z].)[a-zA-Z0-9\-\.]+\.' \
              r'([a-zA-Z0-9\-\.]{2,}))+(\:[0-9]+)*(\/($|[a-zA-Z0-9\.+\,\;\?\'' \
              r'\\\+&amp;%\$#\=~_\-]+))*'


def set_log(verbose, logfile='config.ini'):
    """Create logger, set logging level, read settings from config file.

    :Parameters:
        - 'verbose': boolean.
        - 'logfile': logger configuration file name in 'CONFROOT' folder, e.g.
                     'validator_log.conf'.

    :Return:
        logger object.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    return logger


def parse_url(log, urls, timeout=5):
    """Open url address, parse it for links in 'a' tags with BeautifulSoup, get
    IP for each found URL.

    :Parameters:
        - 'url': URL address.
        - 'timeout': integer.

    :Return:
        list of tuples with found URLs and host IP.
    """
    try:
        page = urllib2.urlopen(urls, None, timeout)
        source = page.read()
        soup = BeautifulSoup(source, 'html.parser')
        url_list = []
        item = soup.title
        print item
        stripped = urls.split('//', 1)[-1].split('/', 1)
        address = socket.gethostbyname(stripped[0])
        url_list.append((item, address))

        return url_list
    except IOError as err:
        log.critical('Error parsing URL %s', err)
        raise MyError('Address reading error: %s' % err)


class ProcessUrl(threading.Thread):

    def __init__(self, url, q, log):
        super(ProcessUrl, self).__init__()
        self.url = url
        self.log = log
        self.queue = q
        self.singlelock = threading.Lock()

    def run(self):
        self.log.info('Checking URL: %s' % self.url)
        pattern = re.compile(URL_PATTERN)
        if re.match(pattern, self.url):
            self.log.info('URL %s is walid' % self.url)

            # addresses = parse_url(self.log, self.url, timeout=25)
            page = urllib2.urlopen(self.url, None, 25)
            source = page.read()
            soup = BeautifulSoup(source, 'html.parser')
            url_list = []
            item = soup.title.string.encode('ascii', 'ignore')
            print item
            stripped = self.url.split('//', 1)[-1].split('/', 1)
            address = socket.gethostbyname(stripped[0])
            url_list.append((item, self.url, address))
            self.queue.put(url_list)
            # self.singlelock.acquire()
            self.log.info('Done!')
            # self.singlelock.release()
        else:
            print 'Wrong URL'
            self.log.critical('Invalid URL')


def main():
    try:
        t = time.time()
        log = set_log(verbose=2)

        urls = ('http://www.google.com', 'http://www.alibaba.com',
                'http://www.ebay.com', 'http://www.amazon.com')

        threads = []

        address_list = []
        queue = Queue.Queue()
        # start all of the threads
        for url in urls:
            thread = ProcessUrl(url, queue, log)
            thread.start()
            threads.append(thread)

        # now wait for them all to finish
        for thread in threads:
            a = queue.get()
            address_list.extend(a)
            thread.join()

        import pprint
        pp = pprint.PrettyPrinter()
        pp.pprint(address_list)
        log.info('Done in %s' % (time.time() - t,))

    except MyError as err:
        print err
    except EOFError:
        print '\n exiting'


if __name__ == '__main__':
    main()
