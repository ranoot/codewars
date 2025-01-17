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

# def generate_primes(m, n, primes = np.array([]), primes_bool = np.array([])): #TODO: Modify this to be suitable for the segmented sieve
#     # primes refer to the list of primes up to m (not inclusive)
#     marks = np.ones(n-m+1, dtype=bool) # boolean array, first element corresponds to 2 (so n -> n - 2 in the indexing)

#     # eliminate all entries based on previous primes.
#     if np.any(primes):
#         for prime in primes:
#             marks[prime - (m % prime):(n-1):prime] = False
    
#     # eliminate more that were not considered in the previous run
#     checked_until = math.ceil(math.sqrt(m))
#     checking_until = math.ceil(math.sqrt(n))
#     print(checked_until, checking_until)
#     for i in range(2 if checked_until <= 2 else checked_until, checking_until + (1 if checked_until == checking_until else 0)):    
#         print(i)
#         if primes_bool[i-2]: #! There should be some segment sizes that do not work with this
#             marks[i - (m % i):(n-1):i] = False
    
#     return marks

# def segmented_prime_sieve(n, limit):
#     marks = np.array([True], dtype=bool)
#     primes = np.array([2])
#     high = 2 # this is inclusive
#     while high < n:
#         new_segment = generate_primes(high+1, high+limit, primes, marks)
#         marks = np.append(marks, new_segment)
#         primes = np.append(primes, np.nonzero(new_segment)[0] + high)
#         high += limit

#     return marks

# print(segmented_prime_sieve(30, 10))

def prime_sieve(n):
    marks = np.ones(n-1, dtype=bool)
    for i in range(2, math.ceil(math.sqrt(n))):
        if marks[i-2]:
            marks[(i*i - 2):(n-1):i] = False
    return marks

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


# phi_cache = {}
# phi_lookup = phi_precompute()
# def phi(x, a, primes):
#     global Q
#     # print(a)
#     """
#     Implementation of the partial sieve function, which
#     counts the number of integers <= x with no prime factor less
#     than or equal to the ath prime.
#     """
#     # If value is cached, just return it
#     if (x, a) in phi_cache: return phi_cache[(x, a)]

#     # Base case: phi(x, a) is the number of odd integers <= x
    
#     if a >= 1 and x < primes[a-1]: return 1
#     if a == 5: 
#         # print(math.floor(x - math.floor(x/Q)*Q))
#         return ((x//Q)*phi_lookup[Q]) + phi_lookup[math.floor(x - (x//Q)*Q)]
#     if a == 0: return math.floor(x)

#     result = phi(x, a-1, primes) - phi(x // primes[a-1], a-1, primes)
#     phi_cache[(x, a)] = result # Memoize
#     return result

@timeit
def count_primes_less_than(n:int) -> int:
    # Calculating primes up to x^(2/3) TODO: check these funcs
    sieved_primes = prime_sieve(math.floor(pow(n, 2/3)))

    p_sqrt = pi(pow(n, 1/2), sieved_primes) # floor + 1 then -2 to convert the indexes
    p_cubert = pi(pow(n, 1/3), sieved_primes) # floor + 1 then -2 to convert the indexes
    
    primes = np.nonzero(sieved_primes)[0] + 2
    # return phi(n, p_sqrt, primes) + p_sqrt - 1
    return phi(n, p_cubert, primes) + p_cubert - 1 - p2(n, p_cubert, primes, sieved_primes, p_sqrt)

class PrimeCounter:
    def __init__(self, upper_limit, c):
        self.sieved_primes = self.prime_sieve(math.floor(pow(upper_limit, 2/3)))
        
        self.primes = np.nonzero(self.sieved_primes)[0] + 2

        self.Q = np.prod(self.primes[:c])
        self.c = c
        self.phi_cache = {}
        self.phi_lookup = self.phi_precompute()
        
    def prime_sieve(self, n):
        marks = np.ones(n-1, dtype=bool)
        for i in range(2, math.ceil(math.sqrt(n))):
            if marks[i-2]:
                marks[(i*i - 2):(n-1):i] = False
        return marks

    def pi(self, x):
        return np.sum(self.sieved_primes[:math.floor(x) - 1])

    def phi_precompute(self):
        def unoptimised_phi(x, a):
                # If value is cached, just return it
            if (x, a) in self.phi_cache: return self.phi_cache[(x, a)]

            # Base case: phi(x, a) is the number of odd integers <= x
            if a==0: return math.floor(x)

            result = unoptimised_phi(x, a-1) - unoptimised_phi(x / self.primes[a-1], a-1)
            self.phi_cache[(x, a)] = result
            return result
        
        lookup_table = {} # a value is implicitly 5
        for x in range(self.Q + 1):
            lookup_table[x] = unoptimised_phi(x, self.c)
        return lookup_table

    def phi(self, x, a):
        # If value is cached, just return it
        if (x, a) in self.phi_cache: return self.phi_cache[(x, a)]

        # We have 2 "truncating rules"
        if a >= 1 and x < self.primes[a-1]: return 1
        if a == 5: # Uses a lookup table to cut-off all the additional branches
            # print(math.floor(x - math.floor(x/Q)*Q))
            return ((x//self.Q)*self.phi_lookup[self.Q]) + self.phi_lookup[math.floor(x - (x//self.Q)*self.Q)]
        if a == 0: return math.floor(x) # if we are computing a small a value > 5 then we need something to fallback to

        result = self.phi(x, a-1) - self.phi(x // self.primes[a-1], a-1)
        self.phi_cache[(x, a)] = result # Memoize
        return result

    # Calculating P_2(x, a), TODO (investigate): Likely some issues with this calculation
    def p2(self, x, a):
        p_sqrt = self.pi(pow(x, 1/2))
        sum = (a*(a-1))//2 - (p_sqrt*(p_sqrt-1))//2
        for p in self.primes[(a):(p_sqrt)]:
            sum += self.pi(x//p)
        return sum

    def count(self, n):
        p_cubert = self.pi(pow(n, 1/3))
        return self.phi(n, p_cubert) + p_cubert - 1 - self.p2(n, p_cubert)


PrimePi = PrimeCounter(10**10, 5)
print(PrimePi.p2(2000, 2))
