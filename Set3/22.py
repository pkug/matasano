#!/usr/bin/env python3
"""."""
import random
import time
import sys

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


time.sleep(random.randint(1, 5))
timestamp = int(time.time())
rng = rng_create(timestamp)
r = range(timestamp - 10000, timestamp + 10000)
out = rng()

p = 0
sys.stdout.write('{: <3s}'.format(str(p) + '%'))
sys.stdout.flush()
sys.stdout.write("\b" * 5)

for i in r:
    rng2 = rng_create(i)
    if out == rng2():
        print("\nSEED:", i)
        print("SEED == TIMESTAMP:", i == timestamp)
        break
    pp = int((i - r.start) * 40 / (r.stop - r.start))
    if pp > p:
        p = pp 
        sys.stdout.write('{: <3s}'.format(str(p) + '%'))
        sys.stdout.flush()
        sys.stdout.write("\b" * 5)

sys.stdout.write("\n")
