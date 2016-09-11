#!/usr/bin/env python3
import sys
from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
with open(sys.argv[1]) as f:
    c = b64decode(f.read())
    key = b'YELLOW SUBMARINE'
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    print(decryptor.update(c))
