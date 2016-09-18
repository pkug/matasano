#!/usr/bin/env python3
"""."""
import os
import socket
import sys
import random
from hashlib import sha1
from binascii import unhexlify as unhex
from Crypto.Cipher import AES

nist_p = ("ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024"
"e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd"
"3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec"
"6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f"
"24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361"
"c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552"
"bb9ed529077096966d670c354e4abc9804f1746c08ca237327fff"
"fffffffffffff")

IV = os.urandom(16)
HOST = '127.0.0.1'
PORT = 2000
#PORT = 1337

p = int.from_bytes(unhex(nist_p), 'little')
g = 2

if len(sys.argv) > 1:
    if sys.argv[1] == '1':
        g = 1
    elif sys.argv[1] == '2':
        g = p
    elif sys.argv[1] == '3':
        g = p-1

print("Using g:", g)

a = random.getrandbits(16) % p
A = pow(g, a, p)

def pkcs7(txt, bsize):
    fill = bsize - (len(txt) % bsize)
    return txt + bytes(fill * [fill])

def encrypt(key, iv, msg):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    s = pkcs7(msg.encode(), 16)
    return iv + cipher.encrypt(s)

def decrypt(key, ctext):
    iv, c = ctext[:16], ctext[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    m = cipher.decrypt(c)
    m = m[:-m[-1]] # remove PKCS7
    return m

with socket.socket() as cs:
    cs.connect((HOST, PORT))
    print('Connected!')
    data = ('%d %d %d' % (p, g, A)).encode()
    cs.sendall(data)
    data = cs.recv(4096)
    B = int(data)
    s = pow(B, a, p)
    key = sha1(('%d' % s).encode()).digest()[:16]
    print("KEY:", key)
    for line in sys.stdin:
        cs.sendall(encrypt(key, IV, line))
        data = cs.recv(4096)
        print(decrypt(key, data))
