#!/usr/bin/env python3
"""."""
import os
import random
from base64 import b64encode, b64decode
from Crypto.Cipher import AES

key = os.urandom(16)
cipher = AES.new(key, AES.MODE_ECB)
xor = lambda b1, b2: bytes(x ^ y for x, y in zip(b1, b2))
blocksize = 16

randstrs = [
        b"MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
        b"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
        b"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
        b"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
        b"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
        b"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
        b"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
        b"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
        b"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
        b"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"
]

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def pkcs7(txt):
    fill = blocksize - (len(txt) % blocksize)
    return txt + bytes(fill * [fill])

def valid_pkcs7(m):
    return 1 <= m[-1] <= blocksize and m[-m[-1]:].count(m[-1]) == len(m[-m[-1]:])

def cbcenc(iv, m):
    blk = cipher.encrypt(xor(m[:16], iv))
    return (iv, blk + cbcenc(blk, m[16:])[1] if len(m) >= 32 else blk)

def cbcdec(iv, c):
    blk = xor(cipher.decrypt(c[:16]), iv)
    return blk + cbcdec(c[:16], c[16:]) if len(c) >= 32 else blk

def encrypt(m):
    return cbcenc(bytes(16), pkcs7(m))

def encrypt_rand():
    return encrypt(random.choice(randstrs))

def oracle(iv, c):
    return valid_pkcs7(cbcdec(iv, c))

# find first padding byte in last block of c
def find_padpos(iv, c):
    ciph = bytearray(iv)
    for i in range(blocksize):
        ciph[i] ^= blocksize
        if not oracle(bytes(ciph), bytes(c)):
            return i or blocksize

# crack the CBC padding oracle
def crack(iv, c):
    ctext = bytearray(iv + c)
    msg = b""
    block = len(ctext) - (blocksize * 2)
    padpos = find_padpos(ctext[block:block+blocksize],
            ctext[block+blocksize:block+blocksize*2])
    while block >= 0:
        iv = ctext[block:block+blocksize]
        ciph = ctext[block+blocksize:block+blocksize*2]
        for pp in range(padpos, 0, -1):
            pad = blocksize - pp

            iv[pp:] = [b ^ pad ^ (pad+1) \
                    for b in iv[pp:]]

            for b in range(256):
                iv[pp-1] = b
                if oracle(bytes(iv), bytes(ciph)):
                    msg = bytes([b ^ (pad+1) ^ ctext[block+pp-1]]) + msg
                    break
        block -= blocksize
        padpos = blocksize
    return msg
        
iv2, c2 = encrypt_rand()
m = crack(iv2, c2)
print(m)
print(b64decode(m))

