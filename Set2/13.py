#!/usr/bin/env python3
"""."""

from functools import reduce
from collections import OrderedDict
import random
import json
import os
from Crypto.Cipher import AES

key = os.urandom(16)
cipher = AES.new(key, AES.MODE_ECB)

def parse_keyval(s):
    d = OrderedDict()
    for kv in s.split('&'):
        tpl = kv.split('=', 1)
        if len(tpl) == 2:
            d[tpl[0]] = tpl[1]
        else:
            continue
    return d

def pkcs7(txt, bsize):
    fill = bsize - (len(txt) % bsize)
    return txt + bytes(fill * [fill])

def encrypt_profile(mail):
    m = 'email={}&uid=10&role=user'.format(mail)
    return cipher.encrypt(pkcs7(m.encode('ascii'), 16))

def decrypt_profile(c):
    p = cipher.decrypt(c)
    p = str(p[:-p[-1]])
    #return parse_keyval(p)
    return p

#print(decrypt_profile(encrypt_profile(profile_for("pkugrinas@gmail.com"))))

# email=XXX@XXXXXX .xx&uid=10&role= user------------
c1 = encrypt_profile('XXX@XXXXXX.xx')

# email=XXX@XXXXX. admin&uid=10role =user-----------
c2 = encrypt_profile('XXX@XXXXX.admin')

print(decrypt_profile(c1))
print(decrypt_profile(c1[0:32] + c2[16:32] + c1[32:48]))

