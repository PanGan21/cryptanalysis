import math
import argparse

from collections import Counter
from string import ascii_lowercase
from typing import Tuple

ALPHABET = ascii_lowercase
ALPHABET_SIZE = 26
LETTER_OCCURRENCE = {'e': 12.7, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75, 's': 6.33, 'h': 6.09,
                     'r': 5.99, 'd': 4.25, 'l': 4.03, 'c': 2.78, 'u': 2.76, 'm': 2.41, 'w': 2.36, 'f': 2.23,
                     'g': 2.02, 'y': 1.97, 'p': 1.93, 'b': 1.29, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15,
                     'q': 0.10, 'z': 0.07}


def cipher(text: str, key: int, decrypt: bool) -> str:
    output = ''

    for char in text:
        # If the character is not in the english alphabet don't change it.
        if char not in ALPHABET:
            output += char
            continue

        index = ord(char.lower()) - ord('a')

        if decrypt:
            new_char = ALPHABET[(index - key) % ALPHABET_SIZE]
        else:
            new_char = ALPHABET[(index + key) % ALPHABET_SIZE]

        # Setting the right case for the letter and adding it to the output
        output += new_char.upper() if char.isupper() else new_char

    return output


def create_brute_force_array(text: str) -> list[str]:
    return [cipher(text, key, True) for key in range(ALPHABET_SIZE)]


def fitting_quotient(text: str) -> float:
    counter = Counter(text)
    dist_text = [counter.get(ch, 0) * 100 / len(text)
                 for ch in LETTER_OCCURRENCE]
    return sum([abs(a - b) for a, b in zip(list(LETTER_OCCURRENCE.values()), dist_text)]) / ALPHABET_SIZE


def brute_force_decipher(text: str) -> Tuple[str, int]:
    outputs = create_brute_force_array(text)
    minimum_frequency = math.inf
    original_text = ''
    encryption_key = 0

    for key, output in enumerate(outputs):
        frequency = fitting_quotient(output)

        if frequency < minimum_frequency:
            minimum_frequency, original_text = frequency, output
            encryption_key = key

    return original_text, encryption_key


def parse() -> argparse.ArgumentParser:
    # Creating the command line argument parser
    parser = argparse.ArgumentParser(
        description='Decrypt/Encrypt Caesar cipher. If no decrypt or encrypt flag is given the default is to encrypt (In case the brute force option is chose there\'s no need to specify any other flag)')
    parser.add_argument(
        'text', type=str, help='The text to be encrypted/decrypted')
    parser.add_argument('-k', '--key', type=int,
                        required=False, help='Key used in the cipher')
    parser.add_argument('-b', '--bruteforce', action='store_true',
                        help='Brute force all options and output a guess using frequency analysis')
    parser.add_argument('-l', '--bruteforcelist', action='store_true',
                        help='Output all brute forced options in addition to the guess (Can only be used with the -b flag)')

    # Creating flags
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--decrypt', action='store_true',
                       help='Decrypt the text given')

    # Returning the parsed arguments
    return parser


def main() -> None:
    # Getting the command line arguments
    configured_parser = parse()
    args = configured_parser.parse_args()

    if args.bruteforce:
        if args.bruteforcelist:
            shifts = create_brute_force_array(args.text)
            for i, shift in enumerate(shifts):
                print(f'Key:{i}, Text: {shift}')
        print('\nGuess:')
        guessed_text, guessed_key = brute_force_decipher(args.text)
        print(f'Text: {guessed_text}\nKey: {guessed_key}')
    else:
        if args.key is None:
            configured_parser.error(
                'Specifying a key (-k) is required when not using brute force options (-b)')
        if args.bruteforcelist:
            configured_parser.error(
                'Cannot use (-l) option when not using (-b) option')
        print(cipher(args.text, args.key, args.decrypt))


if __name__ == '__main__':
    main()
