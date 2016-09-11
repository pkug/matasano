#!/usr/bin/env python3
"""."""
import os
import struct
import random
from sha1 import SHA1 as sha1

KEY = random.choice(list(open('/usr/share/dict/words')))[:-1].encode()
message = b'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon'

def auth(msg):
    return sha1(KEY + msg).digest()

def check(msg, mac):
    return sha1(KEY + msg).digest() == mac

def getpad(s):
    cnt = len(s) * 8
    index = (cnt >> 3) & 0x3f
    padding = b'\x80' + b'\x00' * 63
    padLen = 120 - index
    if index < 56:
        padLen = 56 - index
    return padding[:padLen] + struct.pack('>Q', cnt)

mac = auth(message)

forged = b';admin=true'
regs = struct.unpack('>5I', mac)

# Bruteforce keylen
for i in range(30):
    keypad = b'A' * i
    newmsg = message + getpad(keypad + message) + forged
    count = (len(keypad) + len(newmsg)) * 8
    newmac = sha1(forged, regs, count).digest()
    if check(newmsg, newmac):
        print("NEWMSG:", newmsg)
        print("NEWMAC:", newmac)
        print("len(KEY) == len(keypad):", len(KEY) == len(keypad))
        break
