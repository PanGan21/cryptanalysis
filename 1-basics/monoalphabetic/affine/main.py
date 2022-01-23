def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b//a, b % a
        m, n = x-u*q, y-v*q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return gcd, x, y


def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m


def encrypt(text, key):
    #E = (a*x + b) % 26
    return ''.join([chr(((key[0]*(ord(t) - ord('A')) + key[1]) % 26) + ord('A')) for t in text.upper().replace(' ', '')])


def decrypt(cipher, key):
    # D(E) = (a^-1 * (E - b)) % 26
    return ''.join([chr(((modinv(key[0], 26)*(ord(c) - ord('A') - key[1])) % 26) + ord('A')) for c in cipher])


def main():
    text = 'VAMSI KRISHNA'
    key = [7, 20]

    # calling encryption function
    enc_text = encrypt(text, key)

    print('Encrypted Text: {}'.format(enc_text))

    # calling decryption function
    print('Decrypted Text: {}'.format(decrypt(enc_text, key)))


main()
