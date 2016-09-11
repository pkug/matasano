#!/usr/bin/env python3
"""."""

class BadPad(Exception):
    pass

def pkcs7(txt, bsize):
    fill = bsize - (len(txt) % bsize)
    return txt + bytes(fill * [fill])

def valid_pkcs7(c, bsize):
    #if 1 <= c[-1] <= bsize and all(x == c[-1] for x in c[-c[-1]:]):
    if 1 <= c[-1] <= bsize and c[-c[-1]:].count(c[-1]) == len(c[-c[-1]:]):
        return c[:-c[-1]]
    else:
        raise BadPad

strings = [
        b"ICE ICE BABY\x04\x04\x04\x04",
        b"ICE ICE BABY\x05\x05\x05\x05",
        b"ICE ICE BABY\x01\x02\x03\x04"
]

for s in strings:
    try:
        valid_pkcs7(s, 16)
        print(s, "- valid")
    except BadPad:
        print(s, "- invalid")

