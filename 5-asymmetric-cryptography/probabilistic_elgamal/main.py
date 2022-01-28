import random
import math


def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)


# Determines the modular exponential
def power(a, b, c):
    x = 1
    y = a

    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c
        y = (y * y) % c
        b = int(b / 2)
    return x % c


def generate_key(q):
    key = random.randint(math.pow(10, 20), q)
    while gcd(q, key) != 1:
        key = random.randint(math.pow(10, 20), q)
    return key


def encrypt(message, q, h, g):
    encrypted = []

    k = generate_key(q)
    s = power(h, k, q)
    p = power(g, k, q)

    for i in range(0, len(message)):
        encrypted.append(message[i])

    for i in range(0, len(encrypted)):
        encrypted[i] = s * ord(encrypted[i])

    return encrypted, p


def decrypt(cipher_text, p, key, q):
    plaintext = []
    h = power(p, key, q)
    for i in range(0, len(cipher_text)):
        plaintext.append(chr(int(cipher_text[i]/h)))
    return "".join(plaintext)


def main():
    message = "hello world"

    q = random.randint(math.pow(10, 20), math.pow(10, 50))
    g = random.randint(2, q)

    key = generate_key(q)
    h = power(g, key, q)

    cipher_text, p = encrypt(message, q, h, g)
    print("cipher_text: ", cipher_text)
    print("p: ", p)

    decrypted = decrypt(cipher_text, p, key, q)
    print("decrypted: ", decrypted)


main()
