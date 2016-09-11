#!/usr/bin/env python3
"""."""
import os
from Crypto.Cipher import AES

key = os.urandom(16)
nonce = os.urandom(8)
prepstr = b"comment1=cooking%20MCs;userdata="
apstr = b";comment2=%20like%20a%20pound%20of%20bacon"
xor = lambda b1, b2: bytes(x ^ y for x, y in zip(b1, b2))

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def ctrenc(k, ctr, m):
    cipher = AES.new(k, AES.MODE_ECB)
    n = nonce + ctr.to_bytes(8, 'little')
    blk = xor(m, cipher.encrypt(n))
    r = min(len(m), 16)
    return blk + ctrenc(k, ctr+1, m[r:]) if r else blk

def encrypt(msg):
    s = msg.translate(str.maketrans({';': '', '=': ''}))
    s = prepstr + s.encode('ascii') + apstr
    return ctrenc(key, 0, s)

def decrypt(c):
    m = ctrenc(key, 0, c)
    return m

def isadmin(c):
    return b";admin=true;" in decrypt(c)


c = bytearray(encrypt('.admin.true'))

c[32] ^= ord('.') ^ ord(';') 
c[38] ^= ord('.') ^ ord('=') 

print(decrypt(bytes(c)))
print("ADMIN:", isadmin(bytes(c)))
