#!/usr/bin/env python3
"""."""

import os

from Crypto.Cipher import AES

key = os.urandom(16)
iv = key
prepstr = b"comment1=cooking%20MCs;userdata="
apstr = b";comment2=%20like%20a%20pound%20of%20bacon"
xor = lambda b1, b2: bytes(x ^ y for x, y in zip(b1, b2))

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def pkcs7(txt, bsize):
    fill = bsize - (len(txt) % bsize)
    return txt + bytes(fill * [fill])

def encrypt(msg):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    s = msg.translate(str.maketrans({';': '', '=': ''}))
    s = pkcs7(s.encode('ascii'), 16)
    return cipher.encrypt(s)

def decrypt(c):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    m = cipher.decrypt(c)
    m = m[:-m[-1]]
    return m

def compliant(c):
    m = decrypt(c)
    return "OK" if all(32 < b < 127 for b in m) else m
    return m

print("KEY:", key)

# 3 block msg
msg = "111111111111111122222222222222223333333333333333"
ct = encrypt(msg)
print("ENCRYPTED BLOCKS:", len(ct) // 16)
print("COMPLIANT:", compliant(ct))

modct = ct[0:16] + bytes(16) + ct[0:16] + ct[16:]
err = compliant(modct)
print("COMPLIANT:", err)

print("RECOVERED KEY:", xor(err[0:16], err[32:48]))
