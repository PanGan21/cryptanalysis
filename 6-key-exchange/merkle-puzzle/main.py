from os import urandom
from hashlib import sha1
from random import shuffle, choice

puzzle_size = 2 ** 16


def merkles_puzzle():
    sec = [None] * puzzle_size
    puzzles = [None] * puzzle_size

    for i in range(puzzle_size):
        # secret generation
        sec[i] = urandom(16)

        # secret + index as a pair
        pair = sec[i] + int.to_bytes(i, 4, 'big')
        # pair and sha1
        plaintxt = pair + sha1(pair).digest()

        # encryption process:
        key = urandom(10)
        noise = sha1(key).digest()
        noise += sha1(noise).digest()
        ciphertxt = bytes(i ^ j for i, j in zip(plaintxt, noise))

        # puzzle:
        puzzles[i] = ciphertxt + key[2:]

    # random
    shuffle(puzzles)

    # return
    return sec, puzzles


def solve_puzzle(puzzle):
    ciphertxt = puzzle[:40]
    key = puzzle[40:]

    for i in range(puzzle_size):
        # guess possibilities
        noise = sha1(int.to_bytes(i, 2, 'big') + key).digest()
        noise += sha1(noise).digest()

        # decryption process
        plaintxt = bytes(i ^ j for i, j in zip(ciphertxt, noise))

        # pair
        pair = plaintxt[:20]
        digest = plaintxt[20:]

        # time, key and index
        if sha1(pair).digest() == digest:
            return i, pair[:16], int.from_bytes(pair[16:], 'big')


def main():
    alice_sec, public_puzzles = merkles_puzzle()

    bob_time, bob_secret, public_index = solve_puzzle(choice(public_puzzles))

    print('Secret and index published by BOB')
    print('Full key:', bob_secret)
    print('Public Index:', public_index)
    print('Total steps executed:', bob_time)

    print('Secret shared by ALICE ')
    print('Full key:', alice_sec[public_index])

    total_time, total_puzzles = 0, 0

    for puzzle in public_puzzles:
        adv_time, adv_key, adv_index = solve_puzzle(puzzle)

        total_time += adv_time
        total_puzzles += 1

        if adv_index == public_index:
            print(
                'The secret has been found from Adv in less or equal time tan Bob:', adv_key)
            break

        if total_time > bob_time * 100:
            print('Adv attacks and takes more time than bob!')
            break

    print('searched puzzles:', total_puzzles, 'steps executed:', total_time)


main()
