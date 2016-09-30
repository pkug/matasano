#!/usr/bin/env python3
"""."""
import os
import random
import socket
import getpass
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

HOST = '127.0.0.1'
PORT = 2000

with socket.socket() as cs:
    cs.connect((HOST, PORT))
    #C_I = input('User: ')
    C_P = getpass.getpass().encode()
    C_I = 'mail@example.com'
    #C_P = b'alice'
    a = random.getrandbits(16) % p
    A = pow(g, a, p)
    cs.sendall(('%s %d' % (C_I, A)).encode())
    data = cs.recv(4096)
    S_salt, B, u = (int(p) for p in data.split())
    C_xH = sha256(asbytes(S_salt) + C_P).hexdigest()
    C_x = int(C_xH, 16)
    C_S = pow(B, a + u * C_x, p)
    C_K = sha256(asbytes(C_S)).digest()
    M_C = hmac(C_K, asbytes(S_salt))
    cs.sendall(M_C)
    print(cs.recv(1024))
