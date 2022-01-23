import numpy as np
import pandas as pd
import math
from egcd import egcd

alphabet = "abcdefghijklmnopqrstuvwxyz"

letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


def modmatmul(A, B):
    rows = A.shape[0]
    try:
        col = (B.shape[1])
        res = np.zeros(shape=(rows, col))
    except IndexError:
        col = 1
        res = np.zeros(shape=(rows,))

    if col == 1:
        for i in range(rows):
            res[i] = int(round(np.dot(A[i, :], B))) % 26
    else:
        for i in range(rows):
            for j in range(col):
                a = A[i, :]
                b = B[:, j]
                res[i][j] = int(round(np.dot(A[i, :], B[:, j]) % 26))
    return res


def getsubmatrix(A, noti, notj):
    newA = np.delete(np.delete(A, noti, 0), (notj), 1)
    return newA


def xgcd(b, a):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0


def mulinv(b, n):
    g, x, _ = xgcd(b, n)
    if g == 1:
        return x % n


def modular_inverse(A, detA):
    m = len(A)
    inverse = np.zeros(shape=(m, m))
    detminus1 = mulinv(detA, 26)
    for i in range(m):
        for j in range(m):
            newA = getsubmatrix(A, j, i)
            det1 = np.linalg.det(newA)
            inverse[i][j] = ((-1) ** (i + j) * detminus1 * det1) % 26
    return inverse


def main():
    known_cipher = "vdoshc"
    known_plain = "paymor"

    m = 2

    length = len(known_plain)
    coprime = False
    Pstar = np.zeros(shape=(m, m))
    Cstar = np.zeros(shape=(m, m))

    plainlist = np.zeros(shape=(m, int(len(known_plain)/m)))
    cipherlist = np.zeros(shape=(m, int(len(known_cipher)/m)))
    det = 0

    k = 0
    for j in range(int(length / m)):
        for i in range(m):
            plainlist[i][j] = letter_to_index[known_plain[k]]
            cipherlist[i][j] = letter_to_index[known_cipher[k]]
            k += 1

    for i in range(int(length / m)):
        if coprime is False:
            k = 1
            for j in range(i, int(length / m)):
                temp = plainlist[:, i:m + j:k]
                k += 1
                det = int(round(np.linalg.det(temp) % 26))

                if math.gcd(det, len(alphabet)) == 1:
                    coprime = True
                    Pstar = plainlist[:, i:m + j:k-1]
                    Cstar = cipherlist[:, i:m + j:k-1]
                    break
    if coprime:
        print('Matrice invertibile')

        inverse = modular_inverse(Pstar, det)
        K = modmatmul(Cstar, inverse)
        print("The key is: \n" + str(K))
    else:
        print('Unable to find the key')


main()
