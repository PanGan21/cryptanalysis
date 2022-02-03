import random
import base64
import hashlib
import sys

# g = 15
# p = 1011

# a = 5
# b = 9
# eve = 7

# message = 21

# A = (g**a) % p

# B = (g**b) % p

# Eve1 = (A**eve) % p
# Eve2 = (B**eve) % p

# Key1 = (Eve1**a) % p
# Key2 = (Eve2**b) % p

# print('g: ', g, ' (a shared value), n: ', p, ' (a prime number)')

# print('\n== Random value generation ===')

# print('\nAlice calculates:')
# print('a (Alice random): ', a)
# print('Alice value (A): ', A, ' (g^a) mod p')


# print('\nBob calculates:')
# print('b (Bob random): ', b)
# print('Bob value (B): ', B, ' (g^b) mod p')

# print('\n==Alice sends value to Eve ===')

# print('Eve takes Alice\'s value and calculates: ', Eve1)
# print('Alice gets Eve\'s value and calculates key of: ', Key1)

# print('\n==Bob sends value to Eve ===')

# print('Eve takes Bob\'s value and calculates: ', Eve2)
# print('Bob gets Eve\'s value and calculates key of: ', Key2)


def main():
    g = 15
    p = 1011

    message = 21

    print('g: ', g, ' (a shared value), n: ', p, ' (a prime number)')

    # Alice computes a random a
    a = 5
    # Alice computes (g^b) mod p
    A = (g**a) % p
    print('\nAlice calculates:')
    print('a (Alice random): ', a)
    print('Alice value (A): ', A, ' (g^a) mod p')

    # Alice sends A to Eve
    eve = 7
    Eve1 = (A**eve) % p
    Key1 = (Eve1**a) % p
    print('Eve takes Alice\'s value and calculates: ', Eve1)
    print('Alice gets Eve\'s value and calculates key of: ', Key1)

    # Bob computes a random b
    b = 9
    # Bob computes (g^b) mod p
    B = (g**b) % p
    print('\nBob calculates:')
    print('b (Bob random): ', b)
    print('Bob value (B): ', B, ' (g^b) mod p')

    # Bob sends B to Eve
    Eve2 = (B**eve) % p
    Key2 = (Eve2**b) % p
    print('Eve takes Bob\'s value and calculates: ', Eve2)
    print('Bob gets Eve\'s value and calculates key of: ', Key2)


main()
