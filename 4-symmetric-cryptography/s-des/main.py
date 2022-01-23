# P_8 = [6, 3, 7, 4, 8, 5, 10, 9]
# P_10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
# P_4 = [2, 4, 3, 1]
# IP = [2, 6, 3, 1, 4, 8, 5, 7]
# IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]
# E = [4, 1, 2, 3, 2, 3, 4, 1]
# S_0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
# S_1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]


# # Generic method to permut the given block (list)
# # using the given table (list)
# def permut(block, table):
#     return [block[x-1] for x in table]


# # Left shift a list per 1 element
# def left_shift_list(data):
#     res = data[1:]
#     res.append(data[0])
#     return res


# # XOR operation
# # returns the resulting list
# def xor(t1, t2):
#     return [x ^ y for x, y in zip(t1, t2)]


# def generate_keys(key):
#     generated_keys = []

#     key_arr = [int(char) for char in key]
#     tmp = permut(key_arr, P_10)

#     left = left_shift_list(tmp[:5])
#     right = left_shift_list(tmp[5:])

#     key_1 = permut(left + right, P_8)
#     generated_keys.append(key_1)

#     for i in range(2):
#         left = left_shift_list(left)
#         right = left_shift_list(right)

#     key_2 = permut(left + right, P_8)
#     generated_keys.append(key_2)

#     return generated_keys


# def s_des(message, key, encryption=True):
#     keys = generate_keys(key)
#     msg = [int(char) for char in message]
#     tmp = permut(msg, IP)

#     left = tmp[:4]
#     right = tmp[4:]
#     tmp = permut(right, E)

#     tmp = xor(tmp, keys[0])
#     block = tmp[:4]

#     # Get the row with the first and last bit
#     row = int(str(block[0])+str(block[3]), 2)
#     # Get the column from the 2,3,4,5th bits
#     column = int(''.join([str(x) for x in block[1:][:-1]]), 2)

#     val = S_0[row][column]
#     print(val)
#     # l = permut(tmp[:4], S_0)


# def main():
#     key = "1001000011"
#     message = "00100011"
#     s_des(message, key)
#     pass


# main()

IP = [2, 6, 3, 1, 4, 8, 5, 7]
E = [4, 1, 2, 3, 2, 3, 4, 1]
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
P_10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P_8 = [6, 3, 7, 4, 8, 5, 10, 9]
P_4 = [2, 4, 3, 1]

S_0 = [[1, 0, 3, 2],
       [3, 2, 1, 0],
       [0, 2, 1, 3],
       [3, 1, 3, 2]]

S_1 = [[0, 1, 2, 3],
       [2, 0, 1, 3],
       [3, 0, 1, 0],
       [2, 1, 0, 3]]


def permutate(original, fixed_key):
    new = ''
    for i in fixed_key:
        new += original[i - 1]
    return new


def left_half(bits):
    return bits[:int(len(bits)/2)]


def right_half(bits):
    return bits[int(len(bits)/2):]


def shift(bits):
    rotated_left_half = left_half(bits)[1:] + left_half(bits)[0]
    rotated_right_half = right_half(bits)[1:] + right_half(bits)[0]
    return rotated_left_half + rotated_right_half


def key1(key):
    return permutate(shift(permutate(key, P_10)), P_8)


def key2(key):
    return permutate(shift(shift(shift(permutate(key, P_10)))), P_8)


def xor(bits, key):
    new = ''
    for bit, key_bit in zip(bits, key):
        new += str(((int(bit) + int(key_bit)) % 2))
    return new


def lookup_in_sbox(bits, sbox):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return '{0:02b}'.format(sbox[row][col])


def f_k(bits, key):
    L = left_half(bits)
    R = right_half(bits)
    bits = permutate(R, E)
    bits = xor(bits, key)
    bits = lookup_in_sbox(left_half(bits), S_0) + \
        lookup_in_sbox(right_half(bits), S_1)
    bits = permutate(bits, P_4)
    return xor(bits, L)


def s_des(message, key, encryption=True):
    bits = permutate(message, IP)

    temp = None
    if (encryption is True):
        temp = f_k(bits, key1(key))
    else:
        temp = f_k(bits, key2(key))

    bits = right_half(bits) + temp
    if (encryption is True):
        bits = f_k(bits, key2(key))
    else:
        bits = f_k(bits, key1(key))

    return permutate(bits + temp, IP_INV)


def main():
    key = "1001000011"
    message = "00100011"

    cipher_text = s_des(message, key)
    print(cipher_text)

    decrypted = s_des(cipher_text, key, False)
    print(decrypted)


main()
