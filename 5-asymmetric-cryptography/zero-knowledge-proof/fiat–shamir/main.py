import sys
import random

n = 2**255-19

g = 3

# Alice knows x
x = random.randint(1, 2**80)

# Alice selects v
v = random.randint(1, 2**80)

# Bob knows y
y = pow(g, x, n)

# Alice sends to Bob t
t = pow(g, v, n)

# Bob selects c and sends to Alice
c = random.randint(1, 2**80)

# Alice calculates r and sends it to Bob
r = v - c * x


# Bob computes (g^r) * (y^r)
Result = (pow(g, r, n) * pow(y, c, n)) % n

if (t == Result):
    print('Alice has proven she knows x')
else:
    print('Alice has not proven she knows x')
