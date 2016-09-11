#!/usr/bin/env python3
"""."""
import random
import time
import sys

lsb32 = lambda x: int(0xffffffff & x)

def detemper(y):
    y ^= (y >> 18)
    y ^= (y << 15) & 0xEFC60000
    y ^= (y << 7) & 0x1680
    y ^= (y << 7) & 0xC4000
    y ^= (y << 7) & 0xD200000
    y ^= (y << 7) & 0x90000000
    y ^= (y >> 11) & 0xFFC00000
    y ^= (y >> 11) & 0x3FF800
    y ^= (y >> 11) & 0x7FF
    return y

def temper(y):
    y ^= y >> 11
    y ^= y << 7 & 0x9D2C5680
    y ^= y << 15 & 0xEFC60000
    y ^= y >> 18
    return y

class RNG:
    def __init__(self, seed):
        self.mt = [0] * 624
        self.mt[0] = seed
        self.index = 624
        for i in range(1, 624):
            self.mt[i] = lsb32(1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)

    def rand(self):
        if self.index >= 624:
            self.twist()
        y = temper(self.mt[self.index])
        self.index += 1
        return lsb32(y)

    def twist(self):
        for i in range(624):
            y = lsb32((self.mt[i] & 0x80000000) + 
                      (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = self.mt[(i + 397) % 624] ^ y >> 1
            if y % 2 != 0:
                self.mt[i] ^= 0x9908b0df
        self.index = 0

#r = random.randint(1, 100)
r = 123456

rng = RNG(r)
rng2 = RNG(0)

for i in range(624):
    rng2.mt[i] = detemper(rng.rand())

for i in range(len(rng2.mt)):
    if rng2.mt[i] != rng.mt[i]:
        print(rng2.mt[i], "!=", rng.mt[i], "at:", i)

for i in range(1000):
    a = rng.rand()
    b = rng2.rand()
    if a != b:
        print(a, "!=", b, "at pos:", i)
        break
else:
    print("All good!")
