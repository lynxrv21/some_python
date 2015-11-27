import time
import threading
import urllib2

urls = ['http://www.google.com', 'http://www.amazon.com',
        'http://www.ebay.com', 'http://www.alibaba.com',
        'http://www.reddit.com']
start = time.time()


def get_responses():
    for url in urls:
        resp = urllib2.urlopen(url)
        print url, resp.getcode()
    print "Elapsed time: %s" % (time.time()-start)


class ResponseThread(threading.Thread):
    def __init__(self, url):
        super(ResponseThread, self).__init__()
        self.url = url

    def run(self):
        resp = urllib2.urlopen(self.url)
        print self.url, resp.getcode()


def in_threads():
    threads = []
    for url in urls:
        t = ResponseThread(url)
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    print time.time()-start


if __name__ == '__main__':
    # get_responses()
    in_threads()
