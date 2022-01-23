import utils


def tryGuessingSubstring(substring, message_length, xor_messages):
    good_guesses = []
    for pos in range(message_length - len(substring) + 1):
        guess = utils.toHex(chr(0) * pos + substring + chr(0) *
                            (message_length - len(substring) - pos))
        other_message_part = utils.toStr(utils.xor(guess, xor_messages))[
            pos:pos + len(substring)]
        good_guess = True
        for i in range(len(other_message_part)):
            if not other_message_part[i].isalpha() and not other_message_part[i].isspace():
                good_guess = False
                break
        if good_guess:
            good_guesses.append((guess, pos, other_message_part))

    print("\nGood guesses:")
    for guess in good_guesses:
        print("position: %d, one message part: \"%s\", another message part: \"%s\"" % (
            guess[1], substring, guess[2]))


def main():
    message1 = "steal the secret"
    key = "supersecretverys"
    message2 = "the boy the girl"

    ciphertext1 = utils.xor(utils.toHex(message1), utils.toHex(key))
    ciphertext2 = utils.xor(utils.toHex(message2), utils.toHex(key))

    # Guess a word that might appear in one of the messages
    # e.x. oy the

    # Encode the word from step 1 to a hex string
    # XOR the two cipher-text messages
    xor_messages = utils.xor(utils.toHex(message1), utils.toHex(message2))

    # XOR the hex string from step 2 at each position of the XOR of the two cipher-texts(from step 3)
    # When the result from step 4 is readable text, we guess the English word and expand our crib search. If the result is not readable text, we try an XOR of the crib word at the next position.
    tryGuessingSubstring("oy the ", len(message1), xor_messages)


main()
