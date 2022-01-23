alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
            "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


def encrypt(k, x):
    cipher_text = ""
    for i in list(x):
        enc = (alphabet.index(i) + k) % 26
        cipher_text += alphabet[enc]
    return cipher_text


def decrypt(k, c):
    plain_text = ""
    for i in list(c):
        dec = (alphabet.index(i) - k) % 26
        plain_text += alphabet[dec]
    return plain_text


def main():
    k = 10
    x = "panepistimio"
    cipher_text = encrypt(k, x)
    print(cipher_text)

    plain_text = decrypt(k, cipher_text)
    print(plain_text)


# main()

def attack():
    cipher_text = "vuoukotgozuutusgygy"

    possible_k = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    # make the cipher text indexes in the alphabet
    index_list = []
    for i in list(cipher_text):
        index_list.append(alphabet.index(i))

    for k in possible_k:
        print("For k: ", k, " plain text is: ", decrypt(k, cipher_text))


attack()
