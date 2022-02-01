from os import urandom
from hashlib import sha1
from random import shuffle, choice

puzzle_size = 2 ** 16


def merkles_puzzle():
    secrets = [None] * puzzle_size
    puzzles = [None] * puzzle_size

    for i in range(puzzle_size):
        # generate secret
        secrets[i] = urandom(16)

        # pair = secret|index
        pair = secrets[i] + int.to_bytes(i, 4, 'big')
        # plaintext := pair|sha1(pair)
        plaintext = pair + sha1(pair).digest()

        key = urandom(10)
        noise = sha1(key).digest()
        noise += sha1(noise).digest()
        ciphertext = bytes(i ^ j for i, j in zip(plaintext, noise))

        # puzzle := ciphertext|key
        puzzles[i] = ciphertext + key[2:]

    shuffle(puzzles)
    return secrets, puzzles


def solve_puzzle(puzzle):
    ciphertext = puzzle[:40]
    key = puzzle[40:]

    for i in range(puzzle_size):
        noise = sha1(int.to_bytes(i, 2, 'big') + key).digest()
        noise += sha1(noise).digest()

        plaintext = bytes(i ^ j for i, j in zip(ciphertext, noise))

        pair = plaintext[:20]
        digest = plaintext[20:]

        if sha1(pair).digest() == digest:
            return pair[:16], int.from_bytes(pair[16:], 'big')


def main():
    alice_secrets, public_puzzles = merkles_puzzle()
    bob_secret, public_index = solve_puzzle(choice(public_puzzles))

    print('Bob has secret and publishes index')
    print('key:', bob_secret)
    print('index:', public_index)
    print('Alice has secret')
    print('key:', alice_secrets[public_index])


main()
