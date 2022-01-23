def split_text(message, key):
    return [message[i: i + len(key)]
            for i in range(0, len(message), len(key))]


def encrypt(message, key):
    encrypted = ""

    splitted_message = split_text(message, key)

    k = []
    for letter in key:
        k.append(sorted(key).index(letter))

    index = 0
    for split in splitted_message:
        message_chunk = ""
        for i in k:
            message_chunk += split[i]
        encrypted += message_chunk
        index += len(key)
    return encrypted


def decrypt(cipher_text, key):
    decrypted = ""

    splitted_cipher = split_text(cipher_text, key)

    k = []
    for letter in key:
        k.append(sorted(key).index(letter))

    index = 0
    for split in splitted_cipher:
        message_chunk = ""
        for i in range(len(k)):
            message_chunk += split[k.index(i)]
        decrypted += message_chunk
        index += len(key)
    return decrypted

    pass


def main():
    plain_text = "kryptografisame"
    key = "ctabg"

    cipher_text = encrypt("kryptografisame", "ctabg")
    print(cipher_text)

    decrypted = decrypt(cipher_text, key)
    print(decrypted)


main()
