import math


# Determines if numerator % denominator == 0
def is_divisible(numerator, denominator):
    return numerator % denominator == 0


# Determines q, r given a and n
# for a = q * n + r, 0 <= r <n
def get_quotient_and_remainer(a, n):
    return divmod(a, n)


# Determines the greatest common divisor (gcd) of a, b
def get_greatest_common_divisor(a, b):
    return math.gcd(a, b)


# Determines the greatest common divisor (gcd) of a, b
# using the euclidean algorithm
def euclidean_gcd(a, b):
    if b == 0:
        return a
    else:
        return euclidean_gcd(b, a % b)


# Determines the greatest common divisor (gcd) of a, b
# using the extended euclidean algorithm
def extended_euclidean_gcd(a, b):
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = extended_euclidean_gcd(b % a, a)
    x = y1 - (b//a) * x1
    y = x1

    return gcd, x, y


print(is_divisible(16, 8))
print(get_quotient_and_remainer(16, 8))
print(get_greatest_common_divisor(100, -40))
print(get_greatest_common_divisor(-100, 40))
print(get_greatest_common_divisor(1118, 346))
print(euclidean_gcd(3012, 287))
print(extended_euclidean_gcd(3012, 287))
print(euclidean_gcd(131, 24))
