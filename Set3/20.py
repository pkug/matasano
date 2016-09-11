#!/usr/bin/env python3
"""."""
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
import os
from functools import reduce

ENGLISHFREQ = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228,
    0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025,
    0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987,
    0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
    0.01974, 0.00074
] # a..z

xor = lambda b1, b2: bytes(x ^ y for x, y in zip(b1, b2))
nonce = (0).to_bytes(8, 'little')
blocksize = 16

def get_score(b):
    c = str.lower(chr(b))
    if 97 <= ord(c) <= 122:
        return ENGLISHFREQ[ord(c) - 97]
    elif c in ",/'? ":
        return 0.05
    elif str.isprintable(c):
        return 0.0001
    return 0

keystream = b''

with open('20.txt', 'r') as f:
    ctexts = [b64decode(l) for l in f]

for i in range(len(max(ctexts, key=len))):
    maxscore = (0, 0, b"")
    for k in range(255):
        col = bytes(c[i] ^ k for c in ctexts if len(c) > i) # column
        s = reduce(lambda total, x: get_score(x) + total, col, 0)
        maxscore = max(maxscore, (s, k))
    keystream += bytes([maxscore[1]])

for c in ctexts:
   print(xor(keystream, c)) 
