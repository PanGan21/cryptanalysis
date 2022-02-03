import random
import hashlib
import sys


def main():
    g = 9
    p = 1001

    print('g: ', g, ' (a shared value), n: ', p, ' (a prime number)')

    # Alice computes a random a
    a = random.randint(5, 10)
    # Alice computes (g^b) mod p
    A = (g**a) % p
    print('\nAlice calculates:')
    print('a (Alice random): ', a)
    print('Alice value (A): ', A, ' (g^a) mod p')

    # Alice sends A to Bob

    # Bob computes a random b
    b = random.randint(10, 20)
    # Bob computes (g^b) mod p
    B = (g**b) % p
    print('\nBob calculates:')
    print('b (Bob random): ', b)
    print('Bob value (B): ', B, ' (g^b) mod p')

    # Bob sends B to Alice

    # Alice calculates (B^a) mod p
    keyA = (B**a) % p
    shared_key_A = hashlib.sha256(str(keyA).encode()).hexdigest()
    print('\nAlice calculates:')
    print('Key: ', keyA, ' (B^a) mod p')
    print('Key: ', shared_key_A)

    # Bob calculates (A^b) mod p
    keyB = (A**b) % p
    shared_key_B = hashlib.sha256(str(keyB).encode()).hexdigest()
    print('\nBob calculates:')
    print('Key: ', keyB, ' (A^b) mod p')
    print('Key: ', shared_key_B)

    # Now Alice has should have the same shared key with Bob
    if (shared_key_A == shared_key_B):
        print('\nShared key is the same')
    else:
        print('\nError, Alice does not have the same shared key with Bob')


main()
