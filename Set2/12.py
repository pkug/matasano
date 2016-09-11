#!/usr/bin/env python3
"""."""
import os
import random
from base64 import b64decode
from Crypto.Cipher import AES

key = os.urandom(16)
cipher = AES.new(key, AES.MODE_ECB)
jib = b'''Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK'''

def pkcs7(txt, bsize):
    fill = bsize - (len(txt) % bsize)
    return txt + bytes(fill * [fill])

def encryption_oracle(msg):
    m = pkcs7(msg + b64decode(jib), 16)
    return cipher.encrypt(m)

def detect_sizes(f):
    ss = len(f(b'A'))
    for i in range(2,64):
        s = len(f(b'A' * i))
        if s > ss:
            return (s - ss, ss - i)

def detect_ecb(f, bs):
    ctxt = f(b'A' * bs * 2)
    return ctxt[0:bs] == ctxt[bs:bs*2]

def crack(oracle, secretlen, bs):
    known = b''
    for _ in range(secretlen):
        pad = b'A' * (bs - (len(known) % bs) - 1)
        org = oracle(pad)
        for i in range(256):
            c = oracle(pad + known + bytes([i]))
            if c[0:len(pad) + len(known) + 1] == \
                    org[0:len(pad) + len(known) + 1]:
                        known += bytes([i])
                        break
    return known

blocksize, secretlen = detect_sizes(encryption_oracle)
blocklen = len(encryption_oracle(b''))

print("BLOCKLEN:", blocklen)
print("BLOCKSIZE:", blocksize)
print("SECRETLEN:", secretlen)
print("ECB:", detect_ecb(encryption_oracle, blocksize))
print("SECRET:", crack(encryption_oracle, secretlen, blocksize))
