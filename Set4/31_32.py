#!/usr/bin/env python3
"""."""
import time
import http.client
import bisect
from urllib.parse import urlencode
from itertools import chain, repeat

CONN = http.client.HTTPConnection("127.0.0.1", 8080)
DL = 0.005 # expected delay (~realdelay / 2)
FNAME = 'failas'
HEXCHARS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f']

def getdelays(signature, pos):
    delays = []
    for c in HEXCHARS:
        signature = signature[:pos] + [c]
        req = '/?' + urlencode({'file': FNAME, 'signature': ''.join(signature)})
        start = time.time()
        CONN.request("GET", req)
        res = CONN.getresponse()
        end = time.time()
        bisect.insort(delays, (end - start, c))
    return delays

signature = ['0'] * 40
prevdelays = [(0, '')]
prevcandidates = []
pos = 0

# XXX: "correct" algorithm should probably backtrack more than one pos due to
# channel noise although two wrong guesses are unlikely..
# for practical purposes this approach worked pretty well.

while pos < 40: # SHA1 == 40 hex chars
    delays = getdelays(signature, pos)[-3:]
    if delays[-1][0] >= prevdelays[-1][0] + DL:
        prevdelays = delays
        # XXX: chain and repeat twice to "retry"
        prevcandidates = list(chain.from_iterable(
            repeat(d[1], 2) for d in delays))
        signature[pos] = delays[-1][-1]
        print('GUESSED:', pos, signature[pos])
        pos += 1
    else:
        if not prevcandidates:
            print('ERROR: not enough candidates for last position')
            break
        signature[pos-1] = prevcandidates.pop()
        print('BACKTRACKING:', pos-1, signature[pos-1])
            
print('DIGEST(' + FNAME + ') == ' + ''.join(signature))
