#!/usr/bin/env python3
import sys
from collections import Counter
from binascii import unhexlify
lineno = 1
with open(sys.argv[1]) as f:
    for line in f:
        cipher = unhexlify(line.rstrip('\n'))
        blocks = [cipher[i:i+16] for i in range(0, len(cipher), 16)]
        if len(blocks) != len(set(blocks)):
            print("Duplicate detected at line {}: {}".format(lineno, blocks))
        lineno += 1


