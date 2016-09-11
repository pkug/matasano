#!/usr/bin/env python3
"""."""
from base64 import b64decode
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

key = b'YELLOW SUBMARINE'

cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
decryptor = cipher.decryptor()

xor = lambda b1, b2: bytes(x ^ y for x, y in zip(b1, b2))

def cbcdec(iv, c):
    blk = xor(decryptor.update(c[:16]), iv)
    return blk + cbcdec(c[:16], c[16:]) if len(c) >= 32 else blk

with open(sys.argv[1]) as f:
    cipher = b64decode(f.read())
    print(cbcdec(bytes(16), cipher))


