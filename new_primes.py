import math
import numpy as np
from timer_wrapper import timeit, clock
from itertools import chain
from bisect import bisect

class PrimeCounter:
    THIRD = 1/3
    TWO_THIRD = 2/3
    def __init__(self, upper_limit):
        upper_limit_2_third = int(round(pow(upper_limit, self.TWO_THIRD), 5))
        self.sieved_primes = self.prime_sieve(upper_limit_2_third)
        
        self.primes = np.nonzero(self.sieved_primes)[0] + 2

        upper_limit_third = int(round(pow(upper_limit, self.THIRD), 5))
        self.mu_values = self.compute_mobius(upper_limit_third)

        self.phi_sieve, self.F_array = self.phi_precompute_sieve(upper_limit_2_third, upper_limit_third)
        self.phi_cache = {}

    def prime_sieve(self, n):
        marks = np.ones(n-1, dtype=bool)
        for i in range(2, math.ceil(math.sqrt(n))):
            if marks[i-2]:
                marks[(i*i - 2):(n-1):i] = False
        return marks
    
    def compute_mobius(self, max_value): 
        """
        @max_value: Upper limit of mu values computed (inclusive)
        If we want to know mu(n), index this at n-1
        This computes mu(i) for  1 <= i <= max_value
        """
        # To compute mobius function up to (upper_limit)^(1/3)
        mobius_marks = np.ones(max_value) # The index is just (input) - 1
        for p in self.primes:
            mobius_marks[(p-1):max_value:p] *= -1
        for p in self.primes:
            p_square = p*p
            mobius_marks[(p_square-1):max_value:(p_square)] = 0
        return mobius_marks  

    def phi_precompute_sieve(self, n, a):
        """
        F_array = {(m, f(m), mu(m))}, we will leave out mu(m) as we already have another function that computes that.
        @n: upper limit for integers to be sieved
        @a: upper limit for the primes to be sieved with
        * We need mu function to be defined
        """
        # This must be after self.primes is defined.
        marks = np.ones(n, dtype=bool) # goes from 1 to n
        F_array = []
        sieve_history = []
        for p in self.primes:
            if p > a: break
            # marks[p-1:n:p] = False
            for i in range(p-1, n, p): # The i here refers to the index of the value we want to sieve out.
                if marks[i]: # first time sieving out
                    if i < a: 
                        mu = self.mu_values[i]
                        if mu != 0:
                            F_array.append((i+1, p, mu)) # we only want m from 1 to a, where mu != 0
                    marks[i] = False
            sieve_history.append(np.copy(marks))
        F_array.sort(key=lambda x: x[0])
        return np.array(sieve_history), np.array(F_array, dtype=int)

    def naive_phi(self, y, b): 
        """Must run phi_precompute_sieve beforehand"""
        # if b==0: return int(y)
        # return np.count_nonzero(self.phi_sieve[b-1][:y])
        
        if b==0: return int(y)
        if b in self.phi_cache:
            phi_incomplete_index = bisect(self.phi_cache[b], y, key=lambda x: x[0])
            # print(y, phi_incomplete_index, self.phi_cache[b])
            if phi_incomplete_index == 0:
                _first = np.count_nonzero(self.phi_sieve[b-1][:y])
                self.phi_cache[b].insert(0, (y, _first)) # insert our new computation at the start of a list
                return _first  #the previous y value calculated are all higher than what we needed
            else:
                y_computed, phi_incomplete = self.phi_cache[b][phi_incomplete_index-1]
                _new = phi_incomplete + np.count_nonzero(self.phi_sieve[b-1][y_computed:y])
                self.phi_cache[b].insert(phi_incomplete_index + 1, (y, _new)) 
                return _new
        else:
            _first = np.count_nonzero(self.phi_sieve[b-1][:y])
            self.phi_cache[b] = [(y, _first)]
            return _first

    # @timeit
    def compute_special_leaves(self, x, x_cubert, p_cubert):
        """
        @x_cubert: Cube Root of the x value (of PrimePi.count)
        #### This can only be run after the following are defined:
        * self.primes
        * self.mu_values
        * self.phi_sieve (from using self.phi_precompute)
        * self.F_array (from using self.phi_precompute)
        """
        # We will need to sieve the entire block [1, x^(2/3)]
        # Store all the intermediate computations
        # Compute the F array
        s_2 = 0
        # For each prime, p_b <= x^(1/3), 
        # we find values in F array s.t. f(m) > p_b+1 and mu(m) != 0
        # print(self.F_array[self.F_array[:, 0] <= 6])
        for b, p_b in enumerate(chain([1], self.primes)):
            if b >= x_cubert: break
            
            p_next = self.primes[b] # This is p_b+1

            # clock.start(f"{b}, {p_b}")
            max_index = np.searchsorted(self.F_array[:, 0], x_cubert, side='right')
            applicable_range = self.F_array[:max_index]
            for m, f_m, mu in applicable_range[applicable_range[:, 1] > p_next]: #! This likely contains the performance issue
                if m*p_next <= x_cubert: continue
                y = x//(m*p_next)
                # print(f"p_(b+1) = {p_next} n* = {m}, f({x}/{p_next*m}, {b}) = {-_intermed}")
                s_2 -= mu*self.naive_phi(y, b)
            # clock.stop()
        # Compute the y value using x//(m*p_b+1)
        # Compute phi(y, b) using the sieve => np.nonzero((intermediate result up to p_b) <= y)
        # This requires a snapshot of all the intermediate results of the sieve
        return s_2

    def compute_ordinary_leaves(self, x, x_cubert):
        s_1 = 0
        for n, mu in enumerate(self.mu_values):
            if n + 1 > x_cubert: break
            s_1 += mu * (x//(n+1))

        return s_1


    def pi(self, x):
        return np.count_nonzero(self.sieved_primes[:math.floor(x) - 1])

    def phi(self, x, x_cubert, p_cubert):
        return self.compute_ordinary_leaves(x, x_cubert) + self.compute_special_leaves(x, x_cubert, p_cubert)

    # Calculating P_2(x, a), 
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
    # @timeit
    def count(self, x):
        x_cubert = int(round(pow(x, self.THIRD), 6))
        p_cubert = self.pi(x_cubert)
        # clock.start()
        _phi = self.phi(x, x_cubert, p_cubert)
        # clock.stop()
        # clock.start()
        _p2 = self.p2(x, p_cubert)
        # clock.stop()
        return _phi + p_cubert - 1 - _p2

PrimePi = PrimeCounter(10**(10))