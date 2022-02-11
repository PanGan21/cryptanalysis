alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def main():
    message = "HVSDF CPZSA KWHVG CQWOZ WGAWG HVOHS JSBHI OZZMM CIFIB CIHCT CHVSF DSCDZ SGACB SM"
    for key in range(len(alphabet)):
        decrypted = ""
        print()

        for character in message:
            index = alphabet.find(character)
            new_position = index - key
            if (character in alphabet):
                decrypted += alphabet[new_position]
            else:
                decrypted += character
        print("key", key)
        print("decrypted", decrypted)


main()
