#!/usr/bin/env python3
from itertools import cycle
vig = lambda b1, b2: hex(bytes(x ^ y for (x,y) in zip(b1, cycle(b2))))
print(vig(b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal",
          b"ICE"))
