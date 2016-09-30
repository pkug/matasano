#!/usr/bin/env python3
"""."""
import math
from datetime import datetime
from random import randint

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

maxp = 1000000

prn('Generating primetable for p <', maxp)
primes = sieve(maxp)
prn('Done')

e = 3

prn('Generating 3 different primes and keys')
q = 3 * [0]
p = 3 * [0]
d = 3 * [0]
et = 3 * [0]

i = 0
while i < 3:
    p[i] = primes.pop(randint(0, len(primes)))
    q[i] = primes.pop(randint(0, len(primes)))
    et[i] = (p[i]-1) * (q[i]-1)
    try:
        d[i] = invmod(e, et[i])
    except:
        continue
    i += 1

prn('Done')

n = [pp * qq for pp, qq in zip(p, q)]

#pubkey = (e, n)
#privkey = (d, n)

test = 12345
c_0 = pow(test, e, n[0])
c_1 = pow(test, e, n[1])
c_2 = pow(test, e, n[2])

m_s_0 = n[1] * n[2]
m_s_1 = n[0] * n[2]
m_s_2 = n[0] * n[1]

N_012 = n[0] * n[1] * n[2]

result = ((c_0 * m_s_0 * invmod(m_s_0, n[0])) + \
         (c_1 * m_s_1 * invmod(m_s_1, n[1])) + \
         (c_2 * m_s_2 * invmod(m_s_2, n[2]))) % N_012

root = round(result ** (1 / 3.0))

print('root:', root)
msg = pow(c_1, d[1], n[1])

print('root == msg:', root == msg)
