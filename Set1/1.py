#!/usr/bin/env python3
from binascii import b2a_base64, unhexlify as unhex
r = b2a_base64(unhex("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"))
print(r)
