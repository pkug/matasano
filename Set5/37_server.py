#!/usr/bin/env python3
"""."""
import os
import random
import socket
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

S_I = b'mail@example.com'
S_P = b'PASSWORD'
S_salt = random.getrandbits(8)
S_xH = sha256(asbytes(S_salt) + S_P).hexdigest()
S_x = int(S_xH, 16)
S_v = pow(g, S_x, p)
del S_x
del S_xH

with socket.socket() as ss:
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind((HOST, PORT))
    ss.listen(1)
    print('Listening on %s:%s' % (HOST, PORT))
    conn, addr = ss.accept()
    with conn:
        print('Connected from:', addr)
        data = conn.recv(4096)
        params = data.split()
        A, C_I = int(params[0]), params[1]
        b = random.getrandbits(16) % p
        B = k * S_v + pow(g, b, p)
        conn.sendall(('%d %d' % (B, S_salt)).encode())
        uH = sha256(asbytes(A) + asbytes(B)).hexdigest()
        u = int(uH, 16)
        S_S = pow(A * pow(S_v, u, p), b, p)
        S_K = sha256(asbytes(S_S)).digest()
        M_C = conn.recv(4096)
        print('M_C:', M_C)
        M_S = hmac(S_K, asbytes(S_salt))
        print('M_S:', M_S)
        conn.sendall(b'OK' if M_S == M_C  and C_I == S_I else b'ERROR')
