#!/usr/bin/env python3
"""."""
import os
import random
from hashlib import sha256
from binascii import unhexlify as unhex

nist_p = ("ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024"
"e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd"
"3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec"
"6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f"
"24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361"
"c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552"
"bb9ed529077096966d670c354e4abc9804f1746c08ca237327fff"
"fffffffffffff")

asbytes = lambda x: ('%d' % x).encode()
hmac = lambda key, msg: sha256(key + msg).digest()

p = int.from_bytes(unhex(nist_p), 'little')
g = 2
k = 3

# C - Carol/Client
# S - Steve/Server

C_I = b'mail@example.com'
C_P = b'SUPERSECRET'

# agree: p, g, k

# S
S_I = b'mail@example.com'
S_P = b'SUPERSECRET'
S_salt = os.urandom(8)
S_xH = sha256(S_salt + S_P).hexdigest()
S_x = int(S_xH, 16)
S_v = pow(g, S_x, p)
# save: S_I, S_P, S_salt, S_v

# C->S
a = random.getrandbits(16) % p
A = pow(g, a, p)
# send A, C_I

# S->C
b = random.getrandbits(16) % p
B = k * S_v + pow(g, b, p)
# send B, S_salt

# S, C
uH = sha256(asbytes(A) + asbytes(B)).hexdigest()
u = int(uH, 16)

# C
C_xH = sha256(S_salt + C_P).hexdigest()
C_x = int(C_xH, 16)
C_S = pow(B - k * pow(g, C_x, p), a + u * C_x, p)

C_K = sha256(asbytes(C_S)).digest()

# S
S_S = pow(A * pow(S_v, u, p), b, p)
S_K = sha256(asbytes(S_S)).digest()

# C->S
M_C = hmac(C_K, S_salt)
# send M_C

# S
# verify ...

if hmac(S_K, S_salt) == M_C:
    print("OK")
