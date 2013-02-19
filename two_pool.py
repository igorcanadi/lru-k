from LRUK import LRUKRP
import random

N1 = 100
N2 = 10000
random.seed(20)

def choose_page_randomly(i):
    if i % 2 == 0:
        return random.randint(1, N1)
    else:
        return random.randint(N1, N1 + N2)

# TODO figure out CRP
CRP = 10

print "B\tLRU-1\tLRU-2\tLRU-3"
for B in (60, 80, 100, 120, 140, 160, 180, 200, 250, 300, 350, 400, 450):
    lru = []
    for k in range(1, 4):
        lru.append(LRUKRP(B, k, CRP, None))

    # warm-up period
    for i in range(10 * N1):
        map(lambda l: l.requestPage(choose_page_randomly(i)), lru)
    # clear stats
    map(lambda l: l.clearStats(), lru)
    # real thing
    for i in range(30 * N1):
        map(lambda l: l.requestPage(choose_page_randomly(i)), lru)

    print '%d\t%lf\t%lf\t%lf' % (B, lru[0].getHitRatio(), lru[1].getHitRatio(), lru[2].getHitRatio())

