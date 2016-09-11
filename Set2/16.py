#!/usr/bin/env python3
"""."""

import os

from Crypto.Cipher import AES

blocksize = 16
key = os.urandom(blocksize)
iv = os.urandom(blocksize)
prepstr = b"comment1=cooking%20MCs;userdata="
apstr = b";comment2=%20like%20a%20pound%20of%20bacon"

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
    s = pkcs7(prepstr + s.encode('ascii') + apstr, blocksize)
    return iv + cipher.encrypt(s)

def decrypt(c):
    cipher = AES.new(key, AES.MODE_CBC, c[:blocksize])
    m = cipher.decrypt(c[blocksize:])
    m = m[:-m[-1]]
    return m

def isadmin(c):
    return b";admin=true;" in decrypt(c)

#b1 = list(chunks(decrypt(encrypt('.user.admin')), blocksize))
#print(b1)

c = bytearray(encrypt('.admin.true'))
#print(decrypt(bytes(c)))

# 3rd block 0th and 5th
c[32] ^= ord('.') ^ ord(';') 
c[38] ^= ord('.') ^ ord('=') 

print(decrypt(bytes(c)))
print("ADMIN:", isadmin(bytes(c)))
