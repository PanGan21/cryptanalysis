# Expand permutation to get a 48bits matrix of datas to apply the xor with k
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

# Initial permutation for the datas
PI = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Initial permutation for the key
PC_1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]


# Permutation applied on shifted key to get Ki+1
PC_2 = [14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32]

# Permutation made after each SBox substitution for each round
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

# Determine the shift for each round of keys
SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

S_BOX = [

    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
     ],

    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
     ],

    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
     ],

    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
     ],

    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
     ],

    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
     ],

    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
     ],

    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
     ]
]

# Final permutation for data after the 16 rounds
PI_1 = [40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25]


# Return the binary value as a string of the given size
def binvalue(val, bitsize):
    binval = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
    if len(binval) > bitsize:
        raise "binary value larger than the expected size"
    while len(binval) < bitsize:
        binval = "0"+binval  # Add as many 0 as needed to get the wanted size
    return binval


# Convert a string into a list of bits
def string_to_bit_array(text):
    array = list()
    for char in text:
        # Get the char value on one byte = 8 bits
        binval = binvalue(char, 8)
        array.extend([int(x) for x in list(binval)])
    return array


# Recreate the string from the bit array
def bit_array_to_string(array):
    res = ''.join([chr(int(y, 2)) for y in [''.join([str(x)
                  for x in _bytes]) for _bytes in split_list(array, 8)]])
    return res


# XOR operation
# returns the resulting list
def xor(t1, t2):
    return [x ^ y for x, y in zip(t1, t2)]


# Split a list into sublists of size "n"
def split_list(s, n):
    return [s[k:k+n] for k in range(0, len(s), n)]


# Shift a list of the given value
def shift_list(g, d, n):
    return g[n:] + g[:n], d[n:] + d[:n]


# Generic method to permut the given block (list)
# using the given table (list)
def permut(block, table):
    return [block[x-1] for x in table]


# Generates an array of keys
# The array size is 16 bytes
def generate_keys(key):
    generated_keys = []

    keys = string_to_bit_array(key)

    # Apply initial permutation to the keys
    keys = permut(keys, PC_1)

    # Split it in to (g=LEFT),(d=RIGHT)
    g, d = split_list(keys, 28)

    # Apply the 16 rounds
    for i in range(16):
        g, d = shift_list(g, d, SHIFT[i])
        tmp = g + d
        # Apply the permutation to get the Ki
        k = permut(tmp, PC_2)
        generated_keys.append(k)

    return generated_keys


# Substitutes bytes using SBOX
def substitute(d_expanded):
    # Split bit array into sublist of 6 bits
    sub_blocks = split_list(d_expanded, 6)
    result = []
    for i in range(len(sub_blocks)):
        block = sub_blocks[i]

        # Get the row with the first and last bit
        row = int(str(block[0])+str(block[5]), 2)

        # Get the column from the 2,3,4,5th bits
        column = int(''.join([str(x) for x in block[1:][:-1]]), 2)
        # column = int(str(block[2]) + str(block[3]) +
        #              str(block[4]) + str(block[5]), 2)

        val = S_BOX[i][row][column]
        # Convert the value to binary
        bin_val = binvalue(val, 4)
        result += [int(x) for x in bin_val]
    return result


def des(message, key, encryption=True):
    if len(key) < 8:
        raise "Key Should be 8 bytes long (64 bits)"
    elif len(key) > 8:
        # If key size is above 8bytes, cut to be 8bytes long
        key = key[:8]

    keys = generate_keys(key)

    # Split the text in blocks of 8 bytes so 64 bits
    text_blocks = split_list(message, 8)

    result = list()
    for block in text_blocks:
        block = string_to_bit_array(block)

        # Apply the initial data permutation
        block = permut(block, PI)

        #g(LEFT), d(RIGHT)
        g, d = split_list(block, 32)

        tmp = None
        # 16 rounds
        for i in range(16):
            # Expand d to match Ki size (48bits)
            d_expanded = permut(d, E)
            if (encryption is True):
                # If encrypt use Ki
                tmp = xor(keys[i], d_expanded)
            else:
                # If decrypt start by the last key
                tmp = xor(keys[15 - i], d_expanded)

            tmp = substitute(tmp)
            tmp = permut(tmp, P)
            tmp = xor(g, tmp)
            g = d
            d = tmp
        # Do the last permutation and append the result to result
        result += permut(d+g, PI_1)
    return bit_array_to_string(result)


def main():
    key = "INSECURE"
    message = "VIGENERE"

    cipher_text = des(message, key)
    print(cipher_text)

    print(des(cipher_text, key, False))


main()
