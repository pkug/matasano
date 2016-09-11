#!/usr/bin/env python3
"""."""
import os
import struct
import random
from md4 import MD4 as md4, _pad

KEY = random.choice(list(open('/usr/share/dict/words')))[:-1].encode()
message = b'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon'

def auth(msg):
    m = md4()
    m.update(KEY + msg)
    return m.dgst()

def check(msg, mac):
    m = md4()
    m.update(KEY + msg)
    return m.dgst() == mac

mac = auth(message)
forged = b';admin=true'
regs = struct.unpack('<4I', mac)

# Bruteforce keylen
for i in range(30):
    keypad = b'A' * i
    newkeymsg = _pad(keypad + message) + forged
    bitlen = len(newkeymsg) * 8
    newmsg = newkeymsg[i:]
    m = md4(*regs)
    m.update(forged, bitlen)
    newmac = m.dgst()
    if check(newmsg, newmac):
        print("NEWMSG:", newmsg)
        print("NEWMAC:", newmac)
        print("len(KEY) == len(keypad):", len(KEY) == len(keypad))
        break
