#!/usr/bin/env python3
"""."""
import re
import hashlib
from Crypto.PublicKey import RSA

# conversion lambdas for whatever reason..
btoint = lambda x: int.from_bytes(x, 'big')
inttob = lambda x: x.to_bytes((x.bit_length() + 7) // 8, 'big')

def find_cube_root(n):
    lo = 0
    hi = n
    while lo < hi:
        mid = (lo+hi)//2
        if mid**3 < n:
            lo = mid+1
        else:
            hi = mid
    return lo

def verify_sig(k, m, sig):
    # https://tools.ietf.org/html/rfc2313#section-8.1
    d = b'\x00' + inttob(pow(btoint(sig), 3, k.n))
    # broken implementation which doesn't check if there's no
    # more data after the hash..
    match = re.match(b'^\x00\x01\xff+?\x00(.{20}).*', d, re.S)
    if not match:
        return False
    h = hashlib.sha1()
    h.update(m)
    dgst = h.digest()
    return match.group(1) == dgst


msg = b'hi mom'
key = RSA.generate(2048, e=3)
pub = key.publickey()

h = hashlib.sha1()
h.update(msg)
dig = h.digest()

fblock = b'\x00\x01\xff\x00' + dig + (b'\x00' * (128 - len(dig) - 4))
fb = btoint(fblock)

root = find_cube_root(fb)

print(verify_sig(pub, msg, inttob(root)))

