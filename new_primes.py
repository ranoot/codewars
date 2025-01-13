import math
import numpy as np
from timer_wrapper import timeit, clock

class PrimeCounter:
    THIRD = 1/3
    TWO_THIRD = 2/3
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
    
    def compute_mobius(self, max_value): 
        # To compute mobius function up to (upper_limit)^(1/3)
        mobius_marks = np.ones(max_value) # The index is just (input) - 1
        for p in self.primes:
            mobius_marks[(p-1):max_value:p] *= -1
        for p in self.primes:
            p_square = p*p
            mobius_marks[(p_square-1):max_value:(p_square)] = 0
        return mobius_marks 
    
    def compute_special_leaves(self):
        # We will need to sieve the entire block [1, x^(2/3)]
        # Compute the F array
        # For each prime, p_b <= x^(1/3), 
        # we find values in F array s.t. f(m) > p_b+1 and mu(m) != 0
        # Compute the y value using x//(m*p_b+1)
        # Compute phi(y, b) using the sieve => np.nonzero((intermediate result up to p_b) <= y)
        # This requires a snapshot of all the intermediate results of the sieve

        pass

    def pi(self, x):
        return np.count_nonzero(self.sieved_primes[:math.floor(x) - 1])

    def phi_precompute(self):
        def unoptimised_phi(x, a):
                # If value is cached, just return it
            if (int(x), a) in self.phi_cache: return self.phi_cache[(int(x), a)]

            # Base case: phi(x, a) is the number of odd integers <= x
            if a==0: return math.floor(x)

            result = unoptimised_phi(x, a-1) - unoptimised_phi(x / self.primes[a-1], a-1)
            self.phi_cache[(int(x), a)] = result
            return result
        
        lookup_table = {} # a value is implicitly 5
        for x in range(self.Q + 1):
            lookup_table[x] = unoptimised_phi(x, self.c)
        return lookup_table

    def phi(self, x, a):
        # If value is cached, just return it
        if (int(x), a) in self.phi_cache: return self.phi_cache[(int(x), a)]

        # We have 2 "truncating rules"
        if a >= 1 and x < self.primes[a-1]: return 1
        if a == self.c: # Uses a lookup table to cut-off all the additional branches
            # print(math.floor(x - math.floor(x/Q)*Q))
            return ((x//self.Q)*self.phi_lookup[self.Q]) + self.phi_lookup[math.floor(x - (x//self.Q)*self.Q)]
        if a == 0: return math.floor(x) # if we are computing a small a value > 5 then we need something to fallback to

        result = self.phi(int(x), a-1) - self.phi(x // self.primes[a-1], a-1)
        self.phi_cache[(int(x), a)] = result # Memoize
        return result

    # Calculating P_2(x, a), TODO (investigate): Likely some issues with this calculation
    def p2(self, x, a):
        p_sqrt = self.pi(round(pow(x, 0.5), 6))
        p_sum = (a*(a-1))//2 - (p_sqrt*(p_sqrt-1))//2
        for p in self.primes[(a):(p_sqrt)]:
            p_sum += self.pi(x//p)
        return p_sum
        # p_sum = 0 #TODO can improve performance, we can avoid enumerating through the entire list. Just have a counter that runs from lower to upper
        # lower = self.primes > int(pow(x, self.THIRD))
        # upper = self.primes <= int(pow(x, 0.5))
        # for p in self.primes[np.logical_and(lower, upper)]:
        #     p_sum += (self.pi(x//p) - self.pi(p) + 1)
        # return p_sum
    @timeit
    def count(self, n):
        p_cubert = self.pi(round(pow(n, self.THIRD), 6))
        clock.start()
        _phi = self.phi(n, p_cubert)
        clock.stop()
        # clock.start()
        _p2 = self.p2(n, p_cubert)
        # clock.stop()
        print(_phi, _p2, p_cubert)
        return _phi + p_cubert - 1 - _p2

PrimePi = PrimeCounter(10**10, 6)

# print(PrimePi.count(9880111997))
# print(PrimePi.phi_cache)