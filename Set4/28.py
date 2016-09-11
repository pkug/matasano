#!/usr/bin/env python3
"""."""
import os
from sha1 import SHA1 as sha1

key = bytes(os.urandom(16))

def auth(key, msg):
    return sha1(key + msg.encode()).digest() + msg.encode()

def check(key, msg):
    return sha1(key + msg[20:]).digest() == msg[:20]


m = "Secret message!"
a = auth(key, m)

print("AUTH:", a)
print("CHECK:", check(key, a))
