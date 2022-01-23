import utils

H = ['0x6a09e667', '0xbb67ae85', '0x3c6ef372', '0xa54ff53a',
     '0x510e527f', '0x9b05688c', '0x1f83d9ab', '0x5be0cd19']

K = ['0x428a2f98', '0x71374491', '0xb5c0fbcf', '0xe9b5dba5', '0x3956c25b', '0x59f111f1', '0x923f82a4', '0xab1c5ed5', '0xd807aa98', '0x12835b01', '0x243185be', '0x550c7dc3', '0x72be5d74', '0x80deb1fe', '0x9bdc06a7', '0xc19bf174', '0xe49b69c1', '0xefbe4786', '0x0fc19dc6', '0x240ca1cc', '0x2de92c6f', '0x4a7484aa', '0x5cb0a9dc', '0x76f988da', '0x983e5152', '0xa831c66d', '0xb00327c8', '0xbf597fc7', '0xc6e00bf3', '0xd5a79147', '0x06ca6351', '0x14292967',
     '0x27b70a85', '0x2e1b2138', '0x4d2c6dfc', '0x53380d13', '0x650a7354', '0x766a0abb', '0x81c2c92e', '0x92722c85', '0xa2bfe8a1', '0xa81a664b', '0xc24b8b70', '0xc76c51a3', '0xd192e819', '0xd6990624', '0xf40e3585', '0x106aa070', '0x19a4c116', '0x1e376c08', '0x2748774c', '0x34b0bcb5', '0x391c0cb3', '0x4ed8aa4a', '0x5b9cca4f', '0x682e6ff3', '0x748f82ee', '0x78a5636f', '0x84c87814', '0x8cc70208', '0x90befffa', '0xa4506ceb', '0xbef9a3f7', '0xc67178f2']


# takes list of 32 bits
# convert to string
def bits_to_hex_string(value):
    value = ''.join([str(x) for x in value])
    # creat 4 bit chunks, and add bin-indicator
    binaries = []
    for d in range(0, len(value), 4):
        binaries.append('0b' + value[d:d+4])
    # transform to hexadecimal and remove hex-indicator
    hexes = ''
    for b in binaries:
        hexes += hex(int(b, 2))[2:]
    return hexes


# string characters to unicode values
def string_to_bytes_arr(message):
    charcodes = [ord(c) for c in message]
    # unicode values to 8-bit strings (removed binary indicator)
    bytes = []
    for char in charcodes:
        bytes.append(bin(char)[2:].zfill(8))
    # 8-bit strings to list of bits as integers
    bits = []
    for byte in bytes:
        for bit in byte:
            bits.append(int(bit))
    return bits


def fill_with_zeros(bits, length=8, endian='LE'):
    l = len(bits)
    if endian == 'LE':
        for i in range(l, length):
            bits.append(0)
    else:
        while l < length:
            bits.insert(0, 0)
            l = len(bits)
    return bits


# divides list of bits into desired byte/word splits,
# starting at LSB
def split_data(bits, split_length=8):
    splited = []
    for b in range(0, len(bits), split_length):
        splited.append(bits[b:b+split_length])
    return splited


# convert from hex to python binary string (with cut bin indicator ('0b'))
def hex_to_binary_string(values):
    binaries = [bin(int(v, 16))[2:] for v in values]
    # convert from python string representation to a list of 32 bit lists
    words = []
    for binary in binaries:
        word = []
        for b in binary:
            word.append(int(b))
        words.append(fill_with_zeros(word, 32, 'BE'))
    return words


def process_message(message):
    # translate message into bits
    bits = string_to_bytes_arr(message)
    # message length
    length = len(bits)
    # get length in bits  of message (64 bit block)
    message_len = [int(b) for b in bin(length)[2:].zfill(64)]
    # if length smaller than 448 handle block individually otherwise
    # if exactly 448 then add single 1 and add up to 1024 and if longer than 448
    # create multiple of 512 - 64 bits for the length at the end of the message (big endian)
    if length < 448:
        # append single 1
        bits.append(1)
        # fill zeros little endian wise
        bits = fill_with_zeros(bits, 448, 'LE')
        # add the 64 bits representing the length of the message
        bits = bits + message_len
        # return as list
        return [bits]
    elif length == 448:
        bits.append(1)
        # moves to next message block - total length = 1024
        bits = fill_with_zeros(bits, 1024, 'LE')
        # replace the last 64 bits of the multiple of 512 with the original message length
        bits[-64:] = message_len
        # returns it in 512 bit chunks
        return chunker(bits, 512)
    else:
        bits.append(1)
        # loop until multiple of 512 if message length exceeds 448 bits
        while len(bits) % 512 != 0:
            bits.append(0)
        # replace the last 64 bits of the multiple of 512 with the original message length
        bits[-64:] = message_len
    # returns it in 512 bit chunks
    return split_data(bits, 512)


def sha256(message):
    k = hex_to_binary_string(K)
    h0, h1, h2, h3, h4, h5, h6, h7 = hex_to_binary_string(H)
    chunks = process_message(message)
    for chunk in chunks:
        w = split_data(chunk, 32)
        for _ in range(48):
            w.append(32 * [0])
        for i in range(16, 64):
            s0 = utils.XORXOR(utils.rotr(w[i-15], 7),
                              utils.rotr(w[i-15], 18), utils.shr(w[i-15], 3))
            s1 = utils.XORXOR(utils.rotr(w[i-2], 17),
                              utils.rotr(w[i-2], 19), utils.shr(w[i-2], 10))
            w[i] = utils.add(utils.add(utils.add(w[i-16], s0), w[i-7]), s1)
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7
        for j in range(64):
            S1 = utils.XORXOR(utils.rotr(e, 6), utils.rotr(
                e, 11), utils.rotr(e, 25))
            ch = utils.XOR(utils.AND(e, f), utils.AND(utils.NOT(e), g))
            temp1 = utils.add(
                utils.add(utils.add(utils.add(h, S1), ch), k[j]), w[j])
            S0 = utils.XORXOR(utils.rotr(a, 2), utils.rotr(
                a, 13), utils.rotr(a, 22))
            m = utils.XORXOR(utils.AND(a, b), utils.AND(a, c), utils.AND(b, c))
            temp2 = utils.add(S0, m)
            h = g
            g = f
            f = e
            e = utils.add(d, temp1)
            d = c
            c = b
            b = a
            a = utils.add(temp1, temp2)
        h0 = utils.add(h0, a)
        h1 = utils.add(h1, b)
        h2 = utils.add(h2, c)
        h3 = utils.add(h3, d)
        h4 = utils.add(h4, e)
        h5 = utils.add(h5, f)
        h6 = utils.add(h6, g)
        h7 = utils.add(h7, h)
    digest = ''
    for val in [h0, h1, h2, h3, h4, h5, h6, h7]:
        digest += bits_to_hex_string(val)
    return digest


def main():
    message = "Hello World"
    print(sha256(message))


main()
