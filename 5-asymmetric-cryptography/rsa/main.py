import random


# Checks if num is prime
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True


# Euclid's algorithm for determining the greatest common divisor
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# Finds the multiplicative inverse of two numbers
def multiplicative_inverse(e, r):
    m0 = r
    y = 0
    x = 1

    if (r == 1):
        return 0

    while (e > 1):
        q = e // r
        t = r
        r = e % r
        e = t
        t = y
        y = x - q * y
        x = t
    if (x < 0):
        x = x + m0

    return x


def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('p and q must be prime numbers')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    n = p * q
    phi = (p-1) * (q-1)
    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)
    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))


def encrypt(pk, message):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the message to numbers based on the character using a^b mod m
    cipher_text = [(ord(char) ** key) % n for char in message]
    # Return the array of bytes
    return cipher_text


def decrypt(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return ''.join(plain)


def main():
    message = "hello world"
    p = 263
    q = 269

    public_key, private_key = generate_keypair(p, q)
    print(''.join(map(lambda x: str(x), public_key)),
          ''.join(map(lambda x: str(x), private_key)))
    cipher_text_bytes = encrypt(private_key, message)
    # join the array of bytes to a string
    cipher_string = ''.join(map(lambda x: str(x), cipher_text_bytes))
    print(cipher_string)

    decrypted = decrypt(public_key, cipher_text_bytes)
    print(decrypted)


main()
