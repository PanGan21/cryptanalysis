from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def encrypt(message, key, iv):
    mac_key = get_random_bytes(AES.block_size)

    encryption_cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(message, AES.block_size)
    cipher_text = encryption_cipher.encrypt(padded_message)

    padding_cipher = AES.new(mac_key, AES.MODE_CBC, iv)
    padded = pad(cipher_text, AES.block_size)
    tag = padding_cipher.encrypt((cipher_text)[-AES.block_size:])

    return b64encode(cipher_text).decode(
        "utf-8") + ":" + b64encode(tag).decode("utf-8")


def decrypt(cipher_text, key, iv):
    ciphertext, tag = cipher_text.split(":")

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plain = cipher.decrypt(b64decode(ciphertext))
    return unpad(plain, AES.block_size)


def main():
    message = b"secret"
    key = get_random_bytes(AES.block_size)
    iv = get_random_bytes(AES.block_size)

    cipher_text = encrypt(message, key, iv)
    print(cipher_text)

    decrypted = decrypt(cipher_text, key, iv)
    print(decrypted)


main()
