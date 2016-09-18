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
k = 3

HOST = '127.0.0.1'
PORT = 1337

with socket.socket() as cs:
    cs.connect((HOST, PORT))
    C_I = "mail@example.com"
    a = random.getrandbits(16) % p
    #A = 0
    #A = p
    A = 2 * p
    cs.sendall(('%d %s' % (A, C_I)).encode())
    data = cs.recv(4096)
    B, S_salt = (int(p) for p in data.split())
    uH = sha256(asbytes(A) + asbytes(B)).hexdigest()
    u = int(uH, 16)
    C_S = 0
    C_K = sha256(asbytes(C_S)).digest()
    M_C = hmac(C_K, asbytes(S_salt))
    cs.sendall(M_C)
    print(cs.recv(1024))
