# truth condition is integer 1
def isTrue(x): return x == 1


# simple if
def if_(i, y, z): return y if isTrue(i) else z


# and - both arguments need to be true
def and_(i, j): return if_(i, j, 0)
def AND(i, j): return [and_(ia, ja) for ia, ja in zip(i, j)]


# simply negates argument
def not_(i): return if_(i, 0, 1)
def NOT(i): return [not_(x) for x in i]


# retrun true if either i or j is true but not both at the same time
def xor(i, j): return if_(i, not_(j), j)
def XOR(i, j): return [xor(ia, ja) for ia, ja in zip(i, j)]


# if number of truth values is odd then return true
def xorxor(i, j, l): return xor(i, xor(j, l))
def XORXOR(i, j, l): return [xorxor(ia, ja, la)
                             for ia, ja, la, in zip(i, j, l)]


# get the majority of results, i.e., if 2 or more of three values are the same
def maj(i, j, k): return max([i, j, ], key=[i, j, k].count)


# rotate right
def rotr(x, n): return x[-n:] + x[:-n]


# shift right
def shr(x, n): return n * [0] + x[:-n]


# full binary adder
def add(i, j):
    # takes to lists of binaries and adds them
    length = len(i)
    sums = list(range(length))
    # initial input needs an carry over bit as 0
    c = 0
    for x in range(length-1, -1, -1):
        # add the inout bits with a double xor gate
        sums[x] = xorxor(i[x], j[x], c)
        # carry over bit is equal the most represented, e.g., output = 0,1,0
        # then 0 is the carry over bit
        c = maj(i[x], j[x], c)
    # returns list of bits
    return sums
