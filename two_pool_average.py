from LRUK import LRUKRP
import random
from find_buffer_size import find_buffer_size

N1 = 100
N2 = 10000

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
CRP = 1

sum = [[[0 for x in range(5)] for y in range(13)]for z in range(30)]

innerCount = 0
for count in range(0,30):
    print "run "+str(count)
    random.seed(count*20)
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
        for i in range(10 * N1, 40 * N1):
            map(lambda l: l.requestPage(pages[i]), lru)

        # find B(1) / B(2)
        B1B2 = find_buffer_size(lru[1].getHitRatio(), pages, B) / float(B)

        print '%d\t%.2lf\t%.3lf\t%.3lf\t%.3lf\t%.1lf' % (B, lru[0].getHitRatio(), lru[1].getHitRatio(), lru[2].getHitRatio(), lru[3].getHitRatio(), B1B2)
        sum[count][innerCount][0] = lru[0].getHitRatio()
        sum[count][innerCount][1] = lru[1].getHitRatio()
        sum[count][innerCount][2] = lru[2].getHitRatio()
        sum[count][innerCount][3] = lru[3].getHitRatio()
        sum[count][innerCount][4] = B1B2
        innerCount += 1
    innerCount = 0
        
# print average
print "Average of the 30 seeds"
print "B\tLRU-1\tLRU-2\tLRU-3\tA0\tB1/B2" 
counter = 0
for B in (60, 80, 100, 120, 140, 160, 180, 200, 250, 300, 350, 400, 450):  
    lru1 = 0.0
    lru2 = 0.0
    lru3 = 0.0
    A0 = 0.0
    B1B2 = 0.0
    for i in range(0,30):
        lru1 += sum[i][counter][0]
        lru2 += sum[i][counter][1]
        lru3 += sum[i][counter][2]
        A0 += sum[i][counter][3]
        B1B2 += sum[i][counter][4]
    counter += 1
    print '%d\t%.2lf\t%.3lf\t%.3lf\t%.3lf\t%.1lf' % (B, lru1/30.0, lru2/30.0, lru3/30.0, A0/30.0, B1B2/30.0)
    
