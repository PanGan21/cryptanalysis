def egcd(m, n):
    if n == 0:
        return m
    else:
        r = m % n
        return egcd(n, r)


def multiplicative_inverse(a, b):
    r1 = a
    r2 = b
    s1 = int(1)
    s2 = int(0)
    t1 = int(0)
    t2 = int(1)

    while r2 > 0:
        q = r1//r2
        r = r1-q * r2
        r1 = r2
        r2 = r
        s = s1-q * s2
        s1 = s2
        s2 = s
        t = t1-q * t2
        t1 = t2
        t2 = t

    if t1 < 0:
        t1 = t1 % a

    return (r1, t1)


# Generate encryption key in range 1<e<Pn
def generate_key(phi):
    key = []
    for i in range(2, phi):
        gcd = egcd(phi, i)
        if gcd == 1:
            key.append(i)
    return key


def create_signature(message, d, n):
    return (message**d) % n


def generate_message_using_signature(s, e, n):
    return (s**e) % n


def main():
    message = 34505

    # p and q are large prime numbers
    p = 709
    q = 773
    n = p * q
    phi = (p-1)*(q-1)

    key = generate_key(phi)

    e = int(7)

    r, d = multiplicative_inverse(phi, e)

    if r == 1:
        d = int(d)
        print("decryption key is: ", d)
    else:
        print("Multiplicative inverse for\
        the given encryption key does not \
        exist. Choose a different encryption key ")

    # Signature is created by Alice
    s = create_signature(message, d, n)

    # Alice sends M and S both to Bob
    # Bob generates message M1 using the
    # signature S, Alice's public key e
    # and product n.
    m1 = generate_message_using_signature(s, e, n)

    if message == m1:
        print("Accept message sent")
    else:
        print("Not equal with original")


main()
