#!/usr/bin/env python3
from binascii import hexlify as hex, unhexlify as unhex
from base64 import b64decode
from functools import reduce
from itertools import zip_longest, cycle
import heapq
import sys

KEYSIZES = (2,41)
ENGLISHFREQ = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228,
    0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025,
    0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987,
    0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
    0.01974, 0.00074
] # a..z

vig = lambda txt, key: bytes(x ^ y for (x,y) in zip(txt, cycle(key)))
hamming = lambda s1, s2: sum(bin(c1 ^ c2).count('1') \
        for c1, c2 in zip_longest(s1, s2, fillvalue=0))

# FIXME: a little lame but does the job pretty much..
def get_score(b):
    code = ord(str.lower(chr(b)))
    if 97 <= code <= 122:
        return ENGLISHFREQ[code - 97]
    elif str.isprintable(chr(code)):
        return 0.0005
    return 0

def get_key(cipher):
    maxscore = (0, 0, b"")
    for key in range(255):
        msg = bytes(x ^ key for x in cipher)
        s = reduce(lambda total, x: get_score(x) + total, msg, 0)
        maxscore = max(maxscore, (s, key, msg))
    return chr(maxscore[1]).encode()

def get_keysize(c):
    l = [] 
    for s in range(*KEYSIZES):
        blks = list(zip(*[iter(c)] * s))
        dists = [hamming(c1, c2) / s for c1, c2 in zip(blks[0::2], blks[1::2])]
        avg = sum(dists) / len(dists)
        heapq.heappush(l, (avg, s))
    return heapq.heappop(l)[1]

with open(sys.argv[1], 'r') as f:
    cipher = b64decode(f.read())
    keysize = get_keysize(cipher)
    key = b''.join(get_key(cipher[i::keysize]) for i in range(keysize))
    print(key)
    print(vig(cipher, key))
