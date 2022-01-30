import sys
import random
import hashlib
from aes import encrypt, decrypt

from Crypto.Util.number import getPrime
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

from Crypto.Protocol.KDF import PBKDF2
import binascii


primebits = 64
secret = "Secret"


def main():

    print("=== 1: Bob and Alice generate a key===")
    print(f"Shared password: {secret}")

    s = int(hashlib.md5(secret.encode()).hexdigest(), 16)
    p = getPrime(primebits, randfunc=get_random_bytes)
    g = 3

    a = random.randint(0, p-1)
    b = random.randint(0, p-1)

    A = pow(g, a, p)
    B = pow(g, b, p)

    salt = get_random_bytes(16)
    key = PBKDF2(str(secret), salt, 32, count=1000, hmac_hash_module=SHA256)

    print(f"Key from password: {binascii.hexlify(key)}")

    A_cipher = encrypt(str(A), key)

    print("\n=== 2: Alice generates cipher and sends to Bob===")
    print("\nBob now receives ...")
    B_receive = decrypt(A_cipher, key)

    B_receive = int(B_receive)

    print(
        f"Alice sends: A_cipher={binascii.hexlify(A_cipher)}\nBob receives={B_receive}")

    KeyBob = pow(B_receive, b, p)

    NewKey = PBKDF2(str(KeyBob), salt, 32, count=1000, hmac_hash_module=SHA256)

    print(f"Bob computes New Key as {binascii.hexlify(NewKey)}")

    B_cipher = encrypt(str(B), key)

    print("\n=== 3: Bob recovers shared key and sends back an encrypted challenge ===")
    c1 = "I am Bob"

    c1_cipher = encrypt(c1, NewKey)

    print(
        f"\nBob send B_cipher={binascii.hexlify(B_cipher)}, c1_cipher={binascii.hexlify(c1_cipher)}")

    A_receive = int(decrypt(B_cipher, key))

    Key = pow(A_receive, a, p)

    newkey = PBKDF2(str(Key), salt, 32, count=1000, hmac_hash_module=SHA256)

    print(f"\nAlice computes New key as {binascii.hexlify(newkey)}")

    c1_recover = decrypt(c1_cipher, newkey)

    print("\n=== 4: Alice recovers the challenge with shared key and sends back an encrypted challenge ===")

    print(f"\nAlice recovers the challenge: '{c1_recover}' using New Key")

    print("Now Alice sends to Bob ...")

    c2 = "I am Alice"

    c2_cipher = encrypt(c2, NewKey)

    print(f"\nAlice send c2_cipher={binascii.hexlify(c2_cipher)}")

    print("\n=== 6: Bob recovers the challenge with the new shared key ===")

    print("Now Bob receives  ...")

    c2_recover = decrypt(c2_cipher, newkey)

    print(f"\nBob recovers the challenge: '{c2_recover}' using New Key")


main()
