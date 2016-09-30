#!/usr/bin/env python3
"""."""
import os
import socket
import sys
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
HOST = '127.0.0.1'
REALPORT = 1337
MYPORT = 2000

with socket.socket() as ss:
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind((HOST, MYPORT))
    ss.listen(1)
    print('Listening on %s:%s' % (HOST, MYPORT))
    conn, addr = ss.accept()
    with conn: # client
        print('Connected from:', addr)
        data = conn.recv(4096)
        params = data.split()
        C_I, A = params[0], int(params[1])
        print('User:', C_I)

        b = 2 % p
        B = pow(g, b, p)
        u = 1
        salt = 0
        conn.sendall(('%d %d %d' % (salt, B, u)).encode())
        bsalt = asbytes(salt)

        M_C = conn.recv(4096) # HMAC-SHA256(K, salt)

        print('Cracking...')
        prc = 0
        lines = open('/usr/share/dict/words').readlines()
        for no, w in enumerate(lines):
            S_xH = sha256(bsalt + w[:-1].encode()).hexdigest()
            S_x = int(S_xH, 16)
            S_v = pow(g, S_x, p)
            S_S = pow(A * pow(S_v, u, p), b, p)
            S_K = sha256(asbytes(S_S)).digest()
            M_S = hmac(S_K, bsalt)
            if M_S == M_C:
                print('DONE!')
                print(w[:-1])
                break
            done = round(no / len(lines) * 100, 1)
            if done > prc:
                prc = done
                print('{}%'.format(prc))


