from LRUK import LRUKRP
import random
import numpy as np
from find_buffer_size import find_buffer_size

N1 = 100
N2 = 10000
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
            for i, b in enumerate(self._buffer):
                if b > N1:
                    self._buffer[i] = p
                    return
            self._buffer[random.randint(0, len(self._buffer) - 1)] = p

    def clearStats(self):
        self._reqs = 0
        self._hits = 0

    def getHitRatio(self):
        return float(self._hits) / self._reqs

def choose_page_randomly(i):
    if i % 2 == 0:
        return random.randint(1, N1)
    else:
        return random.randint(N1 + 1, N1 + N2)

CRP = 0

results = [ {}, {}, {}, {} ]

for B in range(60, 450, 40):
    for k in range(3):
        results[k][B] = []
    for runs in range(4):
        lru = []
        for k in range(3):
            lru.append(LRUKRP(B, k + 1, CRP, None))

        pages = []
        for i in range(40 * N1):
            pages.append(choose_page_randomly(i))

        # warm-up period
        for i in range(10 * N1):
            map(lambda l: l.requestPage(pages[i]), lru)
        # clear stats
        map(lambda l: l.clearStats(), lru)
        # real thing
        for i in range(30 * N1):
            map(lambda l: l.requestPage(pages[i + 10 * N1]), lru)
        for k in range(3):
            results[k][B].append(lru[k].getHitRatio())

for k in range(3):
    f = open('data/two_pool_lru%d.dat' % (k + 1), 'w')
    for B, l in sorted(results[k].iteritems()):
        m = np.mean(results[k][B])
        sd = np.std(results[k][B])
        print >> f, B, m, m-sd, m+sd
