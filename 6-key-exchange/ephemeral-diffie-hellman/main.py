import random
import sys


def main():
    p = 67
    g = 34

    # Alice calculates a random x
    x = random.randint(3, p)
    # Alice calculates g^x
    g_x = (g**x) % p
    print('Alice selects:')
    print('g=', g, ', N=', p)
    print('Alice creates:')
    print('x=', x, ', g^x=', g_x)

    # Alice sends to Bob g, N, g^x
    print('\nAlice sends: g, N and g^x\n')

    # Bob calculates a random y
    y = random.randint(3, p)
    # Bob calculates g^y
    g_y = (g**y) % p
    print('Bob creates:')
    print('y=', y, ', g^y=', g_y)

    print()

    shared_key_A = (g_x**y) % p
    print('Shared key: ', shared_key_A)

    shared_key_B = (g_y**x) % p
    print('Shared key: ', shared_key_B)

    # Now Alice has should have the same shared key with Bob
    if (shared_key_A == shared_key_B):
        print('\nShared key is the same')
    else:
        print('\nError, Alice does not have the same shared key with Bob')


main()
