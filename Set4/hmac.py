#!/usr/bin/env python3
"""."""
from sha1 import SHA1 as sha1
from binascii import hexlify

xor = lambda b1, b2: bytes(x ^ y for x, y in zip(b1, b2))

BLOCKSIZE = 64 # SHA1 blocksize

def hmac(key, msg):
    k = sha1(key).digest() if len(key) > BLOCKSIZE \
            else key + bytes(BLOCKSIZE - len(key))
    inner = sha1(xor(k, bytes([0x36] * BLOCKSIZE)) + msg).digest()
    m = xor(k, bytes([0x5c] * BLOCKSIZE)) + inner
    return hexlify(sha1(m).digest())
