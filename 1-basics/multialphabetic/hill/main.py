import numpy as np
from egcd import egcd

alphabet = "abcdefghijklmnopqrstuvwxyz"

letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


def matrix_mod_inv(matrix, modulus):
    # Finds the inverse of a matrix in a modulus

    # Step 1) Find determinant
    det = int(np.round(np.linalg.det(matrix)))

    # Step 2) Find determinant value in a specific modulus (usually length of alphabet)
    det_inv = egcd(det, modulus)[1] % modulus

    # Step 3) Take that det_inv times the det*inverted matrix (this will then be the adjoint) in mod 26
    matrix_modulus_inv = (
        det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    )

    return matrix_modulus_inv


def encrypt(message, key):
    encrypted = ""
    message_in_numbers = []

    # Make message into numbers
    for letter in message:
        message_in_numbers.append(letter_to_index[letter])

    # Split it into size of matrix K
    split_p = [message_in_numbers[i: i + int(key.shape[0])]
               for i in range(0, len(message_in_numbers), int(key.shape[0]))]

    # Iterate through each partial message and encrypt it using K*P (mod 26)
    for p in split_p:
        p = np.transpose(np.asarray(p))[:, np.newaxis]

        while p.shape[0] != key.shape[0]:
            p = np.append(p, 0)[:, np.newaxis]

        numbers = np.dot(key, p) % len(alphabet)
        n = numbers.shape[0]  # length of encrypted message (in numbers)

        # Map it back to text
        for idx in range(n):
            number = int(numbers[idx, 0])
            encrypted += index_to_letter[number]

    return encrypted


def decrypt(cipher_text, key_inv):
    decrypted = ""
    cipher_in_numbers = []

    # Make cipher_text into numbers
    for letter in cipher_text:
        cipher_in_numbers.append(letter_to_index[letter])

    # Split it into size of matrix inv(K) in order to do matrix multiplication
    split_c = [cipher_in_numbers[i: i + int(key_inv.shape[0])]
               for i in range(0, len(cipher_in_numbers), int(key_inv.shape[0]))]

    # Iterate through each partial cipher_text and decrypt it using inv(K)*C (mod 26)
    for c in split_c:
        c = np.transpose(np.asarray(c))[:, np.newaxis]
        numbers = np.dot(key_inv, c) % len(alphabet)
        n = numbers.shape[0]

        # Map it back to text
        for idx in range(n):
            number = int(numbers[idx, 0])
            decrypted += index_to_letter[number]

    return decrypted


def main():
    key = np.array([[11, 6, 8], [0, 3, 14], [24, 0, 9]])
    message = "beontimeatten"

    cipher_text = encrypt(message, key)
    print(cipher_text)

    key_inv = matrix_mod_inv(key, len(alphabet))

    decrypted_text = decrypt(cipher_text, key_inv)
    print(decrypted_text)


main()
