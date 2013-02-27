from LRUK import LRUKRP
import random
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

# TODO figure out CRP
CRP = 10

print "B\tLRU-1\tLRU-2\tLRU-3\tA0\tB1/B2"
for B in (60, 80, 100, 120, 140, 160, 180, 200, 250, 300, 350, 400, 450):
    lru = []
    for k in range(1, 4):
        lru.append(LRUKRP(B, k, CRP, None))
    lru.append(A0(B))

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
        map(lambda l: l.requestPage(pages[i]), lru)

    # find B(1) / B(2)
    B1B2 = find_buffer_size(lru[1].getHitRatio(), pages, B) / float(B)

    print '%d\t%lf\t%lf\t%lf\t%lf\t%lf' % (B, lru[0].getHitRatio(), lru[1].getHitRatio(), lru[2].getHitRatio(), lru[3].getHitRatio(), B1B2)

