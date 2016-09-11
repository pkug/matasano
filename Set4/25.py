#!/usr/bin/env python3
"""."""
import sys
import os
from base64 import b64decode
from Crypto.Cipher import AES

key = b'YELLOW SUBMARINE'
randkey = os.urandom(16)
cipher = AES.new(key, AES.MODE_ECB)
nonce = os.urandom(8)
xor = lambda b1, b2: bytes(x ^ y for x, y in zip(b1, b2))

def ctrenc(k, ctr, m):
    cipher = AES.new(k, AES.MODE_ECB)
    n = nonce + ctr.to_bytes(8, 'little')
    blk = xor(m, cipher.encrypt(n))
    r = min(len(m), 16)
    return blk + ctrenc(k, ctr+1, m[r:]) if r else blk

with open('25.txt') as f:
    c = b64decode(f.read())

plain = cipher.decrypt(c)
ctext = ctrenc(randkey, 0, plain)

def edit(c, off, new):
    m = bytearray(ctrenc(randkey, 0, c))
    m[off:len(new)] = new
    return ctrenc(randkey, 0, m)

tst = edit(ctext, 0, ctext)
print(tst)


