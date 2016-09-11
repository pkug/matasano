#!/usr/bin/env python3
"""."""
import os
import random
from base64 import b64encode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

key = os.urandom(16)
cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
encryptor = cipher.encryptor()
decryptor = cipher.decryptor()
xor = lambda b1, b2: bytes(x ^ y for x, y in zip(b1, b2))

def pkcs7(txt, bsize):
    fill = bsize - (len(txt) % bsize)
    return txt + bytes(fill * [fill])

def cbcenc(iv, m):
    blk = encryptor.update(xor(m[:16], iv))
    return blk + cbcenc(blk, m[16:]) if len(m) >= 32 else blk

def cbcdec(iv, c):
    blk = xor(decryptor.update(c[:16]), iv)
    return blk + cbcdec(c[:16], c[16:]) if len(c) >= 32 else blk


def encryption_oracle(msg):
    msg = os.urandom(10) + msg.encode('ascii') + os.urandom(10)
    m = pkcs7(msg, 16)
    if random.choice((0,1)):
        print("CBC")
        r = cbcenc(bytes(16), m)
    else:
        print("ECB")
        r = encryptor.update(m)
    #print(b64encode(r))
    return r

msg = 'A' * 64
ctxt = encryption_oracle(msg)
print(repr(ctxt))
blocks = [ctxt[i:i+16] for i in range(0, len(ctxt), 16)]
if len(blocks) != len(set(blocks)):
    print("Duplicate detected - possibly a ECB!")


