def main():

    # Alice and Bob agree on n
    n = 101*23

    # Alice secrets
    # They are all coprime to n so they don't share a factor with n
    s1 = 5
    s2 = 7
    s3 = 3

    # Bob generate a1, a2, a3 and sends them to Alice
    # They can only be 0 or 1
    a1 = 1
    a2 = 0
    a3 = 1

    # Alice generates random r
    r = 13

    # Alice calculates x and sends it to Bob
    x = (r**2) % n

    # Bob calculates y and sends it to Alice
    y = (r * ((s1**a1) * (s2**a2) * (s3**a3))) % n

    # Alice calculates v1, v2, v3 and sends them to Bob
    v1 = (s1**2) % n
    v2 = (s2**2) % n
    v3 = (s3**2) % n

    # Bob computes y2
    y2 = (x * ((v1**a1) * (v2**a2) * (v3**a3))) % n

    if (((y**2) % n) == y2):
        print("Alice has proven to Bob that Alice knows the secret values")


main()
