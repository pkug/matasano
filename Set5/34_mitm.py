#!/usr/bin/env python3
"""."""
import os
import socket
import sys
import random
from hashlib import sha1
from binascii import unhexlify as unhex
from Crypto.Cipher import AES

HOST = '127.0.0.1'
REALPORT = 1337
MYPORT = 2000

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
    ss.bind((HOST, MYPORT))
    ss.listen(1)
    print('Listening on %s:%s' % (HOST, MYPORT))
    conn, addr = ss.accept()
    with conn: # A->M
        print('Connected from:', addr)
        params = conn.recv(1024) # A->M: Send "p", "g", "A"
        p, g, A = (int(p) for p in params.split()) 
        with socket.socket() as cs: # M->B
            cs.connect((HOST, REALPORT))
            print('Connected to %s:%s' % (HOST, REALPORT))
            data = ('%d %d %d' % (p, g, p)).encode()
            cs.sendall(data) # M->B: Send "p", "g", "p"
            data = cs.recv(1024) # B->M: Send "B"
            conn.sendall(('%d' % p).encode()) # M->A: Send "p"
            s = 0 # pow(p, privkey, p) = 0
            key = sha1(('%d' % s).encode()).digest()[:16]
            print("KEY:", key)
            while True:
                clientdata = conn.recv(1024)
                print("CLIENT:", decrypt(key, clientdata))
                cs.sendall(clientdata)
                servdata = cs.recv(1024)
                print("SERVER:", decrypt(key, servdata))
                conn.sendall(servdata)

