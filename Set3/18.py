#!/usr/bin/env python3
"""."""
from base64 import b64encode, b64decode
from Crypto.Cipher import AES

xor = lambda b1, b2: bytes(x ^ y for x, y in zip(b1, b2))
c = b64decode(b"L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")
key = b"YELLOW SUBMARINE"
cipher = AES.new(key, AES.MODE_ECB)
nonce = (0).to_bytes(8, 'little')
blocksize = 16

def ctrenc(ctr, m):
    n = nonce + ctr.to_bytes(8, 'little')
    blk = xor(m, cipher.encrypt(n))
    r = min(len(m), 16)
    return blk + ctrenc(ctr+1, m[r:]) if r else blk


print(ctrenc(0, c))
