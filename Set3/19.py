#!/usr/bin/env python3
"""."""
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
import os
from functools import reduce

plains = [
        b"SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==",
        b"Q29taW5nIHdpdGggdml2aWQgZmFjZXM=",
        b"RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==",
        b"RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=",
        b"SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk",
        b"T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==",
        b"T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=",
        b"UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==",
        b"QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=",
        b"T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl",
        b"VG8gcGxlYXNlIGEgY29tcGFuaW9u",
        b"QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==",
        b"QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=",
        b"QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==",
        b"QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=",
        b"QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=",
        b"VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==",
        b"SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==",
        b"SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==",
        b"VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==",
        b"V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==",
        b"V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==",
        b"U2hlIHJvZGUgdG8gaGFycmllcnM/",
        b"VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=",
        b"QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=",
        b"VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=",
        b"V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=",
        b"SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==",
        b"U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==",
        b"U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=",
        b"VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==",
        b"QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu",
        b"SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=",
        b"VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs",
        b"WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=",
        b"SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0",
        b"SW4gdGhlIGNhc3VhbCBjb21lZHk7",
        b"SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=",
        b"VHJhbnNmb3JtZWQgdXR0ZXJseTo=",
        b"QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4="
        ]

ENGLISHFREQ = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228,
    0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025,
    0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987,
    0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
    0.01974, 0.00074
] # a..z

xor = lambda b1, b2: bytes(x ^ y for x, y in zip(b1, b2))
nonce = (0).to_bytes(8, 'little')
blocksize = 16

def ctrenc(k, ctr, m):
    cipher = AES.new(k, AES.MODE_ECB)
    n = nonce + ctr.to_bytes(8, 'little')
    blk = xor(m, cipher.encrypt(n))
    r = min(len(m), 16)
    return blk + ctrenc(k, ctr+1, m[r:]) if r else blk

# FIXME: a little lame but does the job pretty much..
def get_score(b):
    code = ord(str.lower(chr(b)))
    if 97 <= code <= 122:
        return ENGLISHFREQ[code - 97]
    elif str.isprintable(chr(code)):
        return 0.0005
    return 0

key = os.urandom(16)
ctexts = [ctrenc(key, 0, b64decode(m)) for m in plains]

keystream = b''

for i in range(len(max(ctexts, key=len))):
    maxscore = (0, 0, b"")
    for k in range(255):
        msg = bytes(c[i] ^ k for c in ctexts if len(c) > i) # column
        s = reduce(lambda total, x: get_score(x) + total, msg, 0)
        maxscore = max(maxscore, (s, k, msg))
    keystream += bytes([maxscore[1]])

print("KEYSTREAM:", keystream, len(keystream))
for c in ctexts:
   print(xor(keystream, c)) 
