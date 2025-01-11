import math
import numpy as np
from functools import wraps
import time

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

def generate_primes(n, primes = np.array([])): 
    # primes refer to the boolean array that have primes indicated as true, 
    # and how long it has checked until
    marks = np.append(primes, np.ones(n-len(primes)-1, dtype=bool))
    # boolean array, first element corresponds to 2 (so n -> n - 2 in the indexing)
    # last element is n (this results in n-1 elements)
    starting_num = len(primes) + 2
    # eliminate all entries based on previous primes.
    if np.any(primes):
        for p in (np.nonzero(primes)[0] + 2):
            q, r = divmod(starting_num, p)
            first_multiple = starting_num if r==0 else (q+1)*p
            marks[first_multiple-2:(n-1):p] = False
    # eliminate more that were not considered in the previous run
    checked_until = math.ceil(math.sqrt(len(primes) + 1))
    checking_until = math.ceil(math.sqrt(n))
    for i in range(2 if checked_until <= 2 else checked_until, checking_until + (1 if checked_until == checking_until else 0)):
        if marks[i-2]:
            marks[(i*i - 2):(n-1):i] = False
    
    return marks

def prime_sieve(n):
    marks = np.ones(n-1, dtype=bool)
    for i in range(2, math.ceil(math.sqrt(n))):
        if marks[i-2]:
            marks[(i*i - 2):(n-1):i] = False
    return marks

# primes = np.array([], dtype=bool)
@timeit
def _count_primes_less_than(n:int) -> int:
    # global primes
    # if n > len(primes) + 1:
    #     primes = generate_primes(n, primes)
    # return sum(primes[:(n-1)])
    return np.sum(prime_sieve(n))

# We will now implement the Meisser-Lehmer Algorithm, we use a = x^(1/3)

def pi(x, sieved_primes):
    return np.sum(sieved_primes[:math.floor(x) - 1])

# Calculating P_2(x, a)
def p2(x, a, primes, sieved_primes, p_sqrt):
    sum = (a*(a-1))//2 - (p_sqrt*(p_sqrt-1))//2
    for p in primes[(a):(p_sqrt)]:
        sum += pi(x//p, sieved_primes)
    return sum

# Calculating phi
Q = 2*3*5*7*11
def phi_precompute():
    global Q
    sieved_primes = prime_sieve(10**5)
    primes = np.nonzero(sieved_primes)[0] + 2

    phi_cache = {}
    def unoptimised_phi(x, a):
            # If value is cached, just return it
        if (x, a) in phi_cache: return phi_cache[(x, a)]

        # Base case: phi(x, a) is the number of odd integers <= x
        if a==0: return math.floor(x)

        result = unoptimised_phi(x, a-1) - unoptimised_phi(x / primes[a-1], a-1)
        phi_cache[(x, a)] = result
        return result
    
    lookup_table = {} # a value is implicitly 5
    for x in range(Q + 1):
        lookup_table[x] = unoptimised_phi(x, 5)
    return lookup_table


phi_cache = {}
phi_lookup = phi_precompute()
def phi(x, a, primes):
    global Q
    # print(a)
    """
    Implementation of the partial sieve function, which
    counts the number of integers <= x with no prime factor less
    than or equal to the ath prime.
    """
    # If value is cached, just return it
    if (x, a) in phi_cache: return phi_cache[(x, a)]

    # Base case: phi(x, a) is the number of odd integers <= x
    
    if a >= 1 and x < primes[a-1]: return 1
    if a == 5: 
        # print(math.floor(x - math.floor(x/Q)*Q))
        return ((x//Q)*phi_lookup[Q]) + phi_lookup[math.floor(x - (x//Q)*Q)]
    if a == 0: return math.floor(x)

    result = phi(x, a-1, primes) - phi(x // primes[a-1], a-1, primes)
    phi_cache[(x, a)] = result # Memoize
    return result

@timeit
def count_primes_less_than(n:int) -> int:
    # Calculating primes up to x^(2/3) TODO: check these funcs
    sieved_primes = prime_sieve(math.floor(pow(n, 2/3)))

    p_sqrt = pi(pow(n, 1/2), sieved_primes) # floor + 1 then -2 to convert the indexes
    p_cubert = pi(pow(n, 1/3), sieved_primes) # floor + 1 then -2 to convert the indexes
    
    primes = np.nonzero(sieved_primes)[0] + 2
    # return phi(n, p_sqrt, primes) + p_sqrt - 1
    return phi(n, p_cubert, primes) + p_cubert - 1 - p2(n, p_cubert, primes, sieved_primes, p_sqrt)
# n = 2000000
# n = 860155317 # works
n = 433798093 # no works

# print(_count_primes_less_than(n))
print(count_primes_less_than(n))
