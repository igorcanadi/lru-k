from LRUK import LRUKRP
import random
from collections import defaultdict
import sys
import json
import numpy as np

pages = json.loads(open('pages_requested').read())

results = [ {}, {}, {} ]
for B in range(50, 500, 25):
    for k in range(3):
        results[k][B] = []
    lru = []
    for k in range(3):
        lru.append(LRUKRP(B, k + 1, 0, None))

    for i, p in enumerate(pages):
        map(lambda l: l.requestPage(p), lru)
        if i == 1000:
            map(lambda l: l.clearStats(), lru)

    for k in range(3):
        results[k][B].append(lru[k].getHitRatio())

for k in range(3):
    f = open('data/postgres_lru%d.dat' % (k + 1), 'w')
    for B, l in sorted(results[k].iteritems()):
        m = np.mean(results[k][B])
        sd = np.std(results[k][B])
        print >> f, B, m, sd
