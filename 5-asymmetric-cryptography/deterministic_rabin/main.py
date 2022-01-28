import random


def to_binary_string(text):
    return bin(text)[2:]


def pad(plaintext):
    # convert to a bit string
    binary_str = to_binary_string(plaintext)

    # pad the last 5 bits to the end
    output = binary_str + binary_str[-5:]

    # convert back to integer
    return int(output, 2)


# Find SQROOT in Zp where p = 3 mod 4
def sqrt_p_3_mod_4(a, p):
    return pow(a, (p + 1) // 4, p)


# Find SQROOT in Zp where p = 5 mod 8
def sqrt_p_5_mod_8(a, p):
    d = pow(a, (p - 1) // 4, p)
    r = 0
    if d == 1:
        r = pow(a, (p + 3) // 8, p)
    elif d == p - 1:
        r = 2 * a * pow(4 * a, (p - 5) // 8, p) % p

    return r


# Euclid's algorithm for determining the greatest common divisor
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, y, x = egcd(b % a, a)
        return gcd, x - (b // a) * y, y


def encryption(plaintext, n):
    # c = m^2 mod n
    plaintext = pad(plaintext)
    return plaintext ** 2 % n


# decide which answer to choose
def choose(lst):

    for i in lst:
        # convert to a bit string
        plain = to_binary_string(i)[:-5]
        append = to_binary_string(i)[-5:]
        last_5_plain = plain[-5:]

        if (last_5_plain == append):
            return plain


def decryption(a, p, q):
    n = p * q
    r, s = 0, 0

    # find sqrt
    # for p
    if p % 4 == 3:
        r = sqrt_p_3_mod_4(a, p)
    elif p % 8 == 5:
        r = sqrt_p_5_mod_8(a, p)
    # for q
    if q % 4 == 3:
        s = sqrt_p_3_mod_4(a, q)
    elif q % 8 == 5:
        s = sqrt_p_5_mod_8(a, q)

    gcd, c, d = egcd(p, q)
    x = (r * d * q + s * c * p) % n
    y = (r * d * q - s * c * p) % n
    lst = [x, n - x, y, n - y]

    choise = choose(lst)

    return int(choise, 2)


def main():
    msg = 2014
    n = 1936093
    p = 1327
    q = 1459

    cipher_text = encryption(msg, n)
    print("cipher_text: ", cipher_text)

    decrypted = decryption(cipher_text, p, q)
    print("decrypted: ", decrypted)


main()
