#!/usr/bin/env python3
"""."""
import random
from hashlib import sha1
from binascii import unhexlify as unhex

nist_p = ("ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024"
"e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd"
"3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec"
"6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f"
"24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361"
"c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552"
"bb9ed529077096966d670c354e4abc9804f1746c08ca237327fff"
"fffffffffffff")

#p = 37

# https://en.wikipedia.org/wiki/Modular_exponentiation

def mod_pow(b, exp, m):
    if m == 1:
        return 0
    c = 1
    for e_p in range(1, exp+1):
        c = (c * b) % m
    return c

#pow = mod_pow

p = int.from_bytes(unhex(nist_p), 'little')
g = 2

a = random.getrandbits(16) % p
A = pow(g, a, p)

b = random.getrandbits(16) % p
B = pow(g, b, p)

s1 = pow(B, a, p)
s2 = pow(A, b, p)

print('s1 == s2', s1 == s2)

k = sha1(('%d' % s1).encode()).digest()[:16]

print('KEY:', k)

