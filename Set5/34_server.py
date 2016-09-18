#!/usr/bin/env python3
"""."""
import os
import socket
import sys
import random
from hashlib import sha1
from binascii import unhexlify as unhex
from Crypto.Cipher import AES

IV = os.urandom(16)
HOST = '127.0.0.1'
PORT = 1337

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

with socket.socket() as ss:
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind((HOST, PORT))
    ss.listen(1)
    print('Listening on %s:%s' % (HOST, PORT))
    conn, addr = ss.accept()
    with conn:
        print('Connected from:', addr)
        params = conn.recv(4096)
        p, g, A = (int(p) for p in params.split())
        b = random.getrandbits(16) % p
        B = pow(g, b, p)
        conn.sendall(('%d' % B).encode())
        s = pow(A, b, p)
        key = sha1(('%d' % s).encode()).digest()[:16]
        print("KEY:", key)
        while True:
            data = conn.recv(4096)
            if not data: sys.exit(1)
            ptext = decrypt(key, data).decode()[:-1]
            print("DECRYPTED:", ptext)
            conn.sendall(encrypt(key, IV, ptext[::-1]))
