import random
import sys

# p = 67
# g = 34


# # Safe generators for selecting G for a prime of 67:
# # 2   7   11   12   13   18   20   28   31   32   34   41   44   46   48   50   51   57   61   63


# x = random.randint(3, p)
# y = random.randint(3, p)

# G_x = (G**x) % p
# G_y = (G**y) % p


# print('Server selects:')
# print('G=', G, ', N=', p)
# print('Server creates:')
# print('x=', x, ', G^x=', G_x)

# print('Server passes: G, N and G^x')
# print()

# print()
# print('Client creates:')
# print('y=', y, ', G^y=', G_y)

# print()
# shared = (G_x**y) % p
# print('Shared key: ', shared)

# shared = (G_y**x) % p
# print('Shared key: ', shared)


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
