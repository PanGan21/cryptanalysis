# Known plaintet attack
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


# Determines the greatest common divisor (gcd) of a, b
# using the extended euclidean algorithm
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


# Determines the result of modulo m addition
def mod_add(a, b, m):
    return (a + b) % m


# Determines the result of modulo m multiplication
def mod_mul(a, b, m):
    return (a * b) % m


# Determines the modular m multiplicative inverse of a using the egcd
def mod_inv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return
    else:
        return x % m


# Determines the modular m additive inverse of a
def get_modular_additive_inverse(a, m):
    for i in range(m):
        inverse = -a + m * i
        if inverse in range(m):
            return inverse


# Determines x in a * x + b = c (mod m)
def solve_linear_congruence(a, b, c, m):
    # find modular additive inverse of b
    mod_inv_b = get_modular_additive_inverse(b, m)

    c_plus_mod_inv_b = mod_add(c, mod_inv_b, m)

    # now the equation is a * x = c_plus_mod_inv_b (mod m)
    # find the modular multiplicative inverse of a
    mod_multi = mod_inv(a, m)

    # multiply c_plus_mod_inv_b with the mod_multi
    return mod_mul(mod_multi, c_plus_mod_inv_b, m)


def decrypt(cipher, key):
    # replace spaces in cipher text
    cipher = cipher.replace(" ", "")
    return "".join([index_to_letter[(mod_inv(key[0], 26)*(letter_to_index[c] - key[1]) % 26)]
                    for c in cipher])


def main():
    # y = (ax+b) mod 26
    cipher_text = "XBCKQ QLXBC DMLMZ LXBCO KRE"

    known_cipher_text_1 = "C"
    known_plain_text_1 = "E"
    known_cipher_text_2 = "X"
    known_plain_text_2 = "T"

    known_cipher_1 = letter_to_index[known_cipher_text_1]
    known_plain_1 = letter_to_index[known_plain_text_1]
    known_cipher_2 = letter_to_index[known_cipher_text_2]
    known_plain_2 = letter_to_index[known_plain_text_2]

    # 2 = (4a+b) mod 26
    print(known_cipher_1)   # 2
    print(known_plain_1)    # 4

    # 23 = (19a+b) mod 26
    print(known_cipher_2)   # 23
    print(known_plain_2)    # 19

    # linear_congruence
    # (1): 4a + b = 2 mod 26
    # (2): 19a + b = 23 mod 26

    # (1) sub (2) => -15a = -21 mod 26
    x = known_plain_1 - known_plain_2
    y = known_cipher_1 - known_cipher_2

    print(x)  # -15
    print(y)  # -21

    # Find x mod 26
    x = x % 26
    print(x)  # 11

    # Find y mod 26
    y = y % 26
    print(y)  # 5

    # -15a = -21 mod 26 => 11a = 5 mod 26
    a = solve_linear_congruence(11, 0, 5, 26)
    print(a)  # 17

    # a = 17 => (1): 4 * 17 + b = 2 mod 26 => 68 + b = 2 mod 26 => 68 mod 26 + b = 2 mod 26
    # => 16 + b = 2 mod 26
    new_a = (a * known_plain_1) % 26
    print(new_a)  # 16

    # 16 + b = 2 mod 26 => b = (2 - 16) mod 26
    b = (known_cipher_1 - new_a) % 26
    print(b)  # 12

    # a = 17, b = 12
    print("a", a)
    print("b", b)
    # y = (ax+b) mod 26
    # encryption function -> y = (17x + b) mod 26

    # Find the decryption function
    # decryption function -> x = inv(17) * (y - 12) mod 26

    # Inverse of 17
    inv_a = mod_inv(a, 26)
    print(inv_a)  # 23

    # key = [a, b]
    key = [a, b]

    # decryption function -> x = 23 * (y - 12) mod 26
    decrypted = decrypt(cipher_text, key)
    print(decrypted)


main()
