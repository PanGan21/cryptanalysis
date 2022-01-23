import utils


# To encrypt, xor the message with the key and get the ciphertext.
# Before doing that convert them both to hex strings.
# Return the regular string
def encrypt(message, key):
    if len(message) != len(key):
        raise Exception("message and key should have the same length")

    hex_message = utils.toHex(message)
    hex_key = utils.toHex(key)
    cipher_text = utils.xor(hex_message, hex_key)

    return utils.toStr(cipher_text)


# To decrypt, xor the ciphertext with the key.
# Before doing that we need convert key to hex
# Return the regular string
def decrypt(cipher_text, key):
    if len(cipher_text) != len(key):
        raise Exception("cipher text and key should have the same length")

    hex_cipher_text = utils.toHex(cipher_text)
    hex_key = utils.toHex(key)
    plain_text = utils.xor(hex_cipher_text, hex_key)

    return utils.toStr(plain_text)


def main():
    key = "supersecretverys"

    message1 = "steal the secret"

    cipher_text_1 = encrypt(message1, key)
    print(cipher_text_1)

    plain_text_1 = decrypt(cipher_text_1, key)
    print(plain_text_1)

    message2 = "the boy the girl"

    cipher_text_2 = encrypt(message2, key)
    print(cipher_text_2)

    plain_text_2 = decrypt(cipher_text_2, key)
    print(plain_text_2)


main()
