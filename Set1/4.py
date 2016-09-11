#!/usr/bin/env python3
from binascii import hexlify as hex, unhexlify as unhex
from functools import reduce
import sys
import heapq
LETTERPROBS = {'e': 12.702, 't': 9.056, 'a': 8.167, 'o': 7.507, 'i': 6.966,
        'n': 6.749, ' ': 6.5, 's': 6.327, 'h': 6.094, 'r': 5.987} # etc..
scorers = [
        lambda c: LETTERPROBS.get(c, 0),
]
top_scores = []

def max_scores(n, ciph):
    scores = []
    for key in range(255):
        msg = bytes(x ^ key for x in unhex(ciph))
        s = reduce(lambda tot, x: sum(f(chr(x)) for f in scorers) + tot, msg, 0)
        heapq.heappush(scores, (s, key, msg, ciph))
    return heapq.merge(top_scores, heapq.nlargest(n, scores))

with open(sys.argv[1], 'r') as f:
    for line in f:
        top_scores = max_scores(3, line.rstrip('\n'))
for (score, key, msg, ciph) in heapq.nlargest(3, top_scores):
    print(ciph, msg, "SCORE: {}, KEY: {}".format(score, key))
