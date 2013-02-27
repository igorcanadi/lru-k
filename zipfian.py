from LRUK import LRUKRP
import random
from math import log
from find_buffer_size import find_buffer_size
import numpy

a = 0.8
b = 0.2
N = 1000
random.seed(20)

class A0:
    def __init__(self, bufferSize):
        self._buffer = [0] * bufferSize
        self._reqs = 0
        self._hits = 0

    def requestPage(self, p):
        self._reqs += 1
        if p in self._buffer:
            self._hits += 1
            return
            
        if 0 in self._buffer:
            self._buffer[self._buffer.index(0)] = p
        else:
            self._buffer[self._buffer.index(max(self._buffer))] = p

    def clearStats(self):
        self._reqs = 0
        self._hits = 0

    def getHitRatio(self):
        return float(self._hits) / self._reqs

def choose_page_randomly():
    r = random.random()
    for i in range(1, N):
        if r < (float(i) / N) ** (log(a) / log(b)):
            return i
    return N

# TODO figure out CRP
CRP = 10

print "B\tLRU-1\tLRU-2\tA0\tB1/B2"
for B in (40, 60, 80, 100, 120, 140, 160, 180, 200, 300, 500):
    lru = []
    for k in range(1, 3):
        lru.append(LRUKRP(B, k, CRP, None))
    lru.append(A0(B))

    pages = []
    for i in range(4000):
        pages.append(choose_page_randomly())

    # warm-up period
    for i in range(1000):
        map(lambda l: l.requestPage(pages[i]), lru)
    # clear stats
    map(lambda l: l.clearStats(), lru)
    # real thing
    for i in range(3000):
        map(lambda l: l.requestPage(pages[i]), lru)

    # find B(1) / B(2)
    B1B2 = find_buffer_size(lru[1].getHitRatio(), pages, B) / float(B)

    print '%d\t%.2lf\t%.2lf\t%.3lf\t%.1lf' % (B, lru[0].getHitRatio(), lru[1].getHitRatio(), lru[2].getHitRatio(), B1B2)

