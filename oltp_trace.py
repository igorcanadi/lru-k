from LRUK import LRUKRP
import random
from math import log
from collections import defaultdict
import sys

a = 0.8
b = 0.2
N = 1000
random.seed(20)

class LFU:
    def __init__(self, bufferSize):
        self._buffer = [0] * bufferSize
        self._freq = defaultdict(int)
        self._reqs = 0
        self._hits = 0

    def requestPage(self, p):
        self._reqs += 1
        self._freq[p] = self._freq[p] + 1
        if p in self._buffer:
            self._hits += 1
            return
            
        victim = self._buffer[0]
        for q in self._buffer:
            if self._freq[q] < self._freq[victim]:
                victim = q
        self._buffer[self._buffer.index(victim)] = p

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
CRP = 30

if len(sys.argv) < 2:
    print "kita"
    sys.exit()

lines = open(sys.argv[1]).read().split('\n')[:100000]
lines = map(lambda x: x.split(','), lines)
lines = filter(lambda x: x[3] == 'r', lines)
max_page = max(map(lambda x: int(x[1]), lines))
pages = map(lambda x: int(x[0]) * (max_page + 1) + int(x[1]), lines)

print "B\tLRU-1\tLRU-2\tLRU-3\tA0"
for B in (100, 200, 300, 400, 500, 600, 800, 1000, 1200, 1400, 1600, 2000, 3000, 5000):
    lru = []
    for k in range(1, 3):
        lru.append(LRUKRP(B, k, CRP, None))
    lru.append(LFU(B))

    for p in pages:
        map(lambda l: l.requestPage(p), lru)

    print '%d\t%lf\t%lf\t%lf' % (B, lru[0].getHitRatio(), lru[1].getHitRatio(), lru[2].getHitRatio())

