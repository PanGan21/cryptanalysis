import functools


# Converts string to hex
def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)

    return functools.reduce(lambda x, y: x+y, lst)


# Converts hex to string
def toStr(s):
    return s and chr(int(s[:2], base=16)) + toStr(s[2:]) or ''


# Computes XOR of two messages s1 and s2.
# s1 and s2 must have the same length.
def xor(s1, s2):
    res = ""
    for i in range(len(s1)):
        res += format(int(s1[i], 16) ^ int(s2[i], 16), '01x')
    return res
