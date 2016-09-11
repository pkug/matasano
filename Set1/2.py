#!/usr/bin/env python3
from binascii import unhexlify as unhex, hexlify as hex
xor = lambda b1, b2: hex(bytes(x ^ y for (x,y) in zip(unhex(b1), unhex(b2))))
print(xor(b"1c0111001f010100061a024b53535009181c",
          b"686974207468652062756c6c277320657965"))
