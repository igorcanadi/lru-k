from LRUK import LRUKRP
import random
from math import log
from find_buffer_size import find_buffer_size
import numpy as np

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

CRP = 0

results = [ {}, {}, {} ]

for B in range(60, 450, 40):
    for k in range(3):
        results[k][B] = []
    for runs in range(4):
        lru = []
        for k in range(3):
            lru.append(LRUKRP(B, k + 1, CRP, None))

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
            map(lambda l: l.requestPage(pages[i + 1000]), lru)

        for k in range(3):
            results[k][B].append(lru[k].getHitRatio())

for k in range(3):
    f = open('data/zipfian_lru%d.dat' % (k + 1), 'w')
    for B, l in sorted(results[k].iteritems()):
        m = np.mean(results[k][B])
        sd = np.std(results[k][B])
        print >> f, B, m, sd

