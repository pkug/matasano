#!/usr/bin/env python3
"""."""
import os
import random
from base64 import b64decode
from Crypto.Cipher import AES

key = os.urandom(16)
cipher = AES.new(key, AES.MODE_ECB)
randpref = os.urandom(random.randint(1,10))
jib = b'''Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK'''

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def pkcs7(txt, bsize):
    fill = bsize - (len(txt) % bsize)
    return txt + bytes(fill * [fill])

def oracle(msg):
    m = pkcs7(randpref + msg + b64decode(jib), 16)
    return cipher.encrypt(m)

def detect_sizes(f):
    ss = len(f(b'A'))
    for i in range(2,64):
        s = len(f(b'A' * i))
        if s > ss:
            return (s - ss, ss - i)

def detect_prefix(f, bs):
    for i in range(1, bs * 3):
        blocks = list(chunks(f(b'A' * i), bs))
        if len(set(blocks)) != len(blocks):
            return bs - i % bs

def detect_ecb(f, bs):
    ctxt = f(b'A' * bs * 3)
    blocks = list(chunks(ctxt, bs))
    return len(set(blocks)) != len(blocks)

def prefix_oracle(f, bs, preflen):
    def oracle(msg):
        c = f(b'B' * (bs - preflen) + msg)
        return c[bs:]
    return oracle

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

bs, randlen = detect_sizes(oracle)
preflen = detect_prefix(oracle, bs)

print("BLOCKSIZE:", bs)
print("ECB:", detect_ecb(oracle, bs))
print("PREFIXLEN:", preflen)
print("MSG:", crack(prefix_oracle(oracle, bs, preflen), randlen - preflen, bs))
