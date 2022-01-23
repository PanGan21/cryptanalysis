import math


# Determines if n is a prime number
def is_prime(n):
    if n <= 1 or n % 1 > 0:
        return False
    for i in range(2, n//2):
        if n % i == 0:
            return False
    return True


# Determines the factors (not the prime factors) of n
def get_factors(n):
    factors = [1]
    for t in range(2, (math.ceil((n / 2) + 1))):
        if n % t == 0:
            factors.append(t)
    factors.append(n)

    return factors


# Determines the prime factors of n
def get_prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)

    return factors


def main():
    num = 21

    print(is_prime(num))
    factor_list = get_factors(num)
    print(factor_list)
    for factor in factor_list:
        print(is_prime(factor))

    print("***** Primes **")
    prime_factors = get_prime_factors(num)
    print(prime_factors)
    for prime_factor in prime_factors:
        print(is_prime(prime_factor))

    print("Numbers are relative prime if gcd(a, b) = 1")
    a = 22
    b = 2
    print(math.gcd(a, b) == 1)


main()
