#!/usr/bin/env python3
"""."""
from datetime import datetime
from random import choice

def sieve(n):
    sieve = [True] * (n//2)
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i//2]:
            sieve[i*i//2::i] = [False] * ((n-i*i-1)//(2*i)+1)
    return [2] + [2*i+1 for i in range(1,n//2) if sieve[i]]

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def invmod(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

prn = lambda *args: print('{:%H:%M:%S}:'.format(datetime.now()), *args)
asint = lambda b: int(b.hex(), 16)
asbytes = lambda i: bytes.fromhex(format(i, 'x'))

maxp = 1000000

prn('Generating primetable for p <', maxp)
primes = sieve(maxp)
prn('Done')

e = 3

while True:
    p, q = choice(primes), choice(primes)
    et = (p-1) * (q-1)
    assert(p != q)
    try:
        d = invmod(e, et)
    except:
        continue
    break

prn('p', p, 'q:', q)

n = p * q

# public key
pubkey = (e, n)

# private key
privkey = (d, n)

# API
encrypt = lambda k, m: [pow(x, k[0], k[1]) for x in m]
decrypt = lambda k, c: b''.join(bytes([pow(x, k[0], k[1])]) for x in c)

test = b'This is the secret message.'
ctxt = encrypt(pubkey, test)
msg = decrypt(privkey, ctxt)

prn('VERIFY:', test == msg)
