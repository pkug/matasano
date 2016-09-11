#!/usr/bin/env python3
"""."""
def pkcs7(txt, bsize):
    fill = bsize - (len(txt) % bsize)
    return txt + bytes(fill * [fill])
txt = b"YELLOW SUBMARINE"
print(pkcs7(txt, 20))

