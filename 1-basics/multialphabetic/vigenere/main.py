alphabet = "abcdefghijklmnopqrstuvwxyz"

letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


def encrypt(message, key):
    encrypted = ''
    # split the message to the length of the key
    splitted_message = [message[i:i + len(key)]
                        for i in range(0, len(message), len(key))]

    # convert the message to index and add the key (mod 26)
    for split in splitted_message:
        i = 0
        for letter in split:
            numeric_letter = (
                letter_to_index[letter] + letter_to_index[key[i]]) % len(alphabet)
            encrypted += index_to_letter[numeric_letter]
            i += 1
    return encrypted


def decrypt(cipher_text, key):
    decrypted = ''

    # split the cipher_text to the length of the key
    splitted_cipher_text = [
        cipher_text[i:i + len(key)] for i in range(0, len(cipher_text), len(key))]

    # convert cipher_text to index and subtract the key (mod 26)
    for split in splitted_cipher_text:
        i = 0
        for letter in split:
            numeric_letter = (
                letter_to_index[letter] - letter_to_index[key[i]]) % len(alphabet)
            decrypted += index_to_letter[numeric_letter]
            i += 1
    return decrypted


def main():
    key = "secret"
    plain_text = "panos"
    cipher_text = encrypt(plain_text, key)
    print(cipher_text)

    decrypted = decrypt(cipher_text, key)
    print(decrypted)


main()
