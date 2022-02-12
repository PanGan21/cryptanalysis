import math
import random
import functools


# Determines if a and b are conruent modulo m
def are_integers_congruent(a, b, m):
    (_, rem_a) = divmod(a, m)
    (_, rem_b) = divmod(b, m)
    return rem_a == rem_b


# Determines the result of modulo m addition
def mod_add(a, b, m):
    return (a + b) % m


# Determines the result of modulo m subtraction
def mod_sub(a, b, m):
    return (a - b) % m


# Determines the result of modulo m multiplication
def mod_mul(a, b, m):
    return (a * b) % m


# Determines the modular m additive inverse of a
def get_modular_additive_inverse(a, m):
    for i in range(m):
        inverse = -a + m * i
        if inverse in range(m):
            return inverse


# Determines the modular m multiplicative inverse of a
def get_modular_multiplicative_inverse(a, m):
    for x in range(1, m):
        if((a % m)*(x % m) % m == 1):
            return x


# Determines the greatest common divisor (gcd) of a, b
# using the extended euclidean algorithm
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


# Determines the modular m multiplicative inverse of a using the egcd
def mod_inv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return
    else:
        return x % m


# Determines x in a * x + b = c (mod m)
def solve_linear_congruence(a, b, c, m):
    # find modular additive inverse of b
    mod_inv_b = get_modular_additive_inverse(b, m)

    c_plus_mod_inv_b = mod_add(c, mod_inv_b, m)

    # now the equation is a * x = c_plus_mod_inv_b (mod m)
    # find the modular multiplicative inverse of a
    mod_multi = mod_inv(a, m)

    # multiply c_plus_mod_inv_b with the mod_multi
    return mod_mul(mod_multi, c_plus_mod_inv_b, m)


# Determines the result of x^y (mod p)
# using sqaure and multiply method
def solve_exponential_congruence(x, y, p):
    res = 1     # Initialize result

    # Update x if it is more
    # than or equal to p
    x = x % p

    if (x == 0):
        return 0

    while (y > 0):
        # If y is odd, multiply
        # x with result
        if ((y & 1) == 1):
            res = (res * x) % p

        # y must be even now
        y = y >> 1      # y = y/2
        x = (x * x) % p

    return res


# Determines euler's φ(n)
def phi(n):
    amount = 0
    for k in range(1, n + 1):
        if math.gcd(n, k) == 1:
            amount += 1
    return amount


# Determines the multiplicative order of a modulo n
# it is the smallest positive integer k with a^k( mod N ) = 1, ( 0 < K < N )
def multiplicative_order(a, n):
    if (math.gcd(a, n) != 1):
        return -1

    # result store power of a that rised
    # to the power N-1
    result = 1

    i = 1
    while (i < n):
        # modular arithmetic
        result = (result * a) % n
        # return smallest + ve integer
        if (result == 1):
            return i
        # increment power
        i = i + 1
    return -1


# Determines the factor values a, b
# and  returns a+b and a-b
def fermat(n):
   # for odd positive integers only
    if(n <= 0):
        return [n]

    # check if n is a even number
    if(n & 1) == 0:
        return [n / 2, 2]

    a = math.ceil(math.sqrt(n))

    # if n is a perfect root,
    # then both its square roots are its factors
    if(a * a == n):
        return [a, a]

    while(True):
        b1 = a * a - n
        b = int(math.sqrt(b1))
        if(b * b == b1):
            break
        else:
            a += 1
    return [a-b, a + b]


# Determines if two numbers are co prime
def are_numbers_coprime(a, b):
    return math.gcd(a, b) == 1


# Determines the primitive roots of modulo m
def get_primitive_roots(m):
    coprime_set = {num for num in range(1, m) if math.gcd(num, m) == 1}
    return [g for g in range(1, m) if coprime_set == {pow(g, powers, m)
            for powers in range(1, m)}]


# Determines a k such that a^k = b (mod m)
# where a and m are relatively prime.
def discrete_logarithm(a, b, m):
    n = int(math.sqrt(m) + 1)

    value = [0] * m

    # Store all values of a^(n*i) of LHS
    for i in range(n, 0, -1):
        value[solve_exponential_congruence(a, i * n, m)] = i

    for j in range(n):

        # Calculate (a ^ j) * b and check
        # for collision
        cur = (solve_exponential_congruence(a, j, m) * b) % m

        # If collision occurs i.e., LHS = RHS
        if (value[cur]):
            ans = value[cur] * n - j

            # Check whether ans lies below m or not
            if (ans < m):
                return ans
    return -1


# Iterative Function to calculate
# (a^n)%p in O(logy)
def power(a, n, p):
    res = 1
    # Update 'a' if 'a' >= p
    a = a % p

    while n > 0:
        # If n is odd, multiply
        # 'a' with result
        if n % 2:
            res = (res * a) % p
            n = n - 1
        else:
            a = (a ** 2) % p
            # n must be even now
            n = n // 2
    return res % p


# If n is prime, then always returns true,
# If n is composite than returns false with
# high probability Higher value of k increases
# probability of correct result
def is_prime_fermat_test(n, k):
    if n == 1 or n == 4:
        return False
    elif n == 2 or n == 3:
        return True

    # Try k times
    else:
        for i in range(k):
            # Pick a random number
            # in [2..n-2]
            # Above corner cases make
            # sure that n > 4
            a = random.randint(2, n - 2)
            # Fermat's theorem
            if power(a, n - 1, n) != 1:
                return False
    return True


# Generates safe prime
# random should be replaced to be secure
def get_safe_primes(n):
    test = 0
    while test != 1:
        q = random.getrandbits(n-1)
        if is_prime_fermat_test(q, n) == 1:
            p = (2 * q) + 1
            test = is_prime_fermat_test(p, n)
    return (p, q)


# Determines ths solution to the system of type x = m (mod a)
# where m, a lists with same length
# using the chinese remainder algorithm
def chinese_remainder(m, a):
    sum = 0
    prod = functools.reduce(lambda acc, b: acc*b, m)
    for n_i, a_i in zip(m, a):
        p = prod // n_i
        sum += a_i * mod_inv(p, n_i) * p
    return sum % prod


# Returns true if there exists an integer
# x such that (x*x)%p = n%p
# using Euler's criterio
def square_root_exists(n, p):
    # Check for Euler's criterion that is
    # [n ^ ((p-1)/2)] % p is 1 or not.
    if (power(n, (int)((p - 1) / 2), p) == 1):
        return True
    return False


# Returns the legendre symbol a|p
# using the Euler's criterio
# p is a prime, a is
# relatively prime to p (if p divides
# a, then a|p = 0)
# Returns 1 if a has a square root modulo
# p, -1 otherwise.
def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)

    if (ls != p - 1):
        return -1
    return ls


# Returns the jacobi symbol
# n must be a positive odd number
def jacobi_symbol(a, n):
    a %= n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a /= 2
            n_mod_8 = n % 8
            if n_mod_8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    if n == 1:
        return result
    else:
        return 0


def main():
    print(are_integers_congruent(2, -3, 5))
    print(get_modular_additive_inverse(44, 13))
    print(get_modular_multiplicative_inverse(11, 21))
    print(get_modular_additive_inverse(1, 10))
    print(get_modular_multiplicative_inverse(9, 10))
    print(get_modular_multiplicative_inverse(13, 22))
    print(solve_linear_congruence(9, 1, 4, 10))
    print(solve_linear_congruence(4, 2, 1, 7))
    print(get_modular_multiplicative_inverse(3, 10))
    print(egcd(131, 24))
    print(solve_exponential_congruence(120, 13, 333))
    for i in range(11, 21):
        print(phi(i))
    print(multiplicative_order(4, 11))
    print(solve_exponential_congruence(7, 5, 12))
    print(fermat(103591*104729))
    print(get_primitive_roots(11))
    print(discrete_logarithm(2, 3, 5))
    print(get_safe_primes(44))
    print(chinese_remainder([3, 4, 7], [1, 1, 0]))
    print(are_numbers_coprime(20, 21))
    print(legendre_symbol(89, 2431))
    print(jacobi_symbol(411247, 55419))


main()
