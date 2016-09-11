#!/usr/bin/env python3
from binascii import hexlify as hex, unhexlify as unhex
from functools import reduce
import bisect
LETTERPROBS = {'e': 12.702, 't': 9.056, 'a': 8.167, 'o': 7.507, 'i': 6.966,
        'n': 6.749, ' ': 6.5, 's': 6.327, 'h': 6.094, 'r': 5.987} # etc..
cipher = b"1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
scorers = [
        lambda c: LETTERPROBS.get(c, 0),
]
scores = []
for key in range(255):
    msg = bytes(x ^ key for x in unhex(cipher))
    s = reduce(lambda total, x: sum(f(chr(x)) for f in scorers) + total, msg, 0)
    bisect.insort_right(scores, (s, key, msg))

for (score, key, msg) in scores[:-5:-1]:
    print(msg, "SCORE: {}, KEY: {}".format(score, key))


