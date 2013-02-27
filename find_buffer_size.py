from LRUK import LRUKRP

N1 = 100

def get_cache_hit_rate(lru1, pages):
    for i in range(10 * N1):
        lru1.requestPage(pages[i])
    # clear stats
    lru1.clearStats()
    # real thing
    for i in range(30 * N1):
        lru1.requestPage(pages[i])
    return lru1.getHitRatio()

def find_buffer_size(cache_hit, pages, min_buffer):
    l = min_buffer
    r = 4 * min_buffer

    while l != r:
        p = (l + r) / 2
        t = get_cache_hit_rate(LRUKRP(p, 1, 10, None), pages)
        if t < cache_hit:
            l = p + 1
        else:
            r = p

    return l
