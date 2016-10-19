#!/usr/bin/env python3
"""."""
import random
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes
from json import dumps

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def invmod(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

# we don't know this
d = {
    'time': 1356304276,
    'social': '555-55-5555',
}

blob = dumps(d)
key = RSA.generate(2048)

# server
c = key.encrypt(blob.encode(), 0)[0]
pub = key.publickey()

# attack
e = pub.e
n = pub.n

# random s to form different message hash
s = random.randint(1, 1000) % n
cc = (pow(s, e, n) * bytes_to_long(c)) % n

# submit cc to server which allows one-time decryption of unique ctexts
pp = key.decrypt(cc)

p = pp * invmod(s, n) % n

print(long_to_bytes(p))
