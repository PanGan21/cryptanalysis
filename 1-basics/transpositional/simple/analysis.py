import itertools

alphabet = "abcdefghijklmnopqrstuvwxyz"


def split_text(message, key):
    return [message[i: i + len(key)]
            for i in range(0, len(message), len(key))]


def brute_force(cipher_text):
    for key_size in range(len(cipher_text)):
        if key_size < 2:
            continue

        if len(cipher_text) % key_size != 0:
            # cheat a bit
            continue

        key = list(range(0, key_size))
        splitted_cipher = split_text(cipher_text, key)

        permutations = list(itertools.permutations(key))

        for perm in permutations:
            dec = ""
            index = 0
            for split in splitted_cipher:
                message_chunk = ""
                for i in range(len(perm)):
                    message_chunk += split[perm.index(i)]
                dec += message_chunk
                index += len(key)
            if dec == "kryptografisame":
                print("Found key")
                print(list(perm))
                print(dec)


brute_force("ytkrprfogaaeism")
