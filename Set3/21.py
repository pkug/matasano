#!/usr/bin/env python3
"""."""

lsb32 = lambda x: int(0xffffffff & x)

def rng_create(seed):
    mt = [seed] + [0] * 623
    index = 624
    for i in range(1, 624):
        mt[i] = lsb32(1812433253 * (mt[i - 1] ^ mt[i - 1] >> 30) + i)

    def extract():
        nonlocal index
        if index >= 623:
            twist()
        y = mt[index]
        y = y ^ y >> 11
        y = y ^ y << 7 & 2636928640
        y = y ^ y << 15 & 4022730752
        y = y ^ y >> 18
        index += 1
        return lsb32(y)
        
    def twist():
        nonlocal index
        for i in range(624):
            y = lsb32((mt[i] & 0x80000000) + \
                      (mt[(i + 1) % 624] & 0x7fffffff))
            mt[i] = mt[(i + 397) % 624] ^ y >> 1
            if y % 2:
                mt[i] ^= 0x9908b0df
        index = 0

    return extract


from datetime import datetime
rng = rng_create(datetime.now().microsecond)
#rng = rng_create(0)
for i in range(10):
    print(rng())
