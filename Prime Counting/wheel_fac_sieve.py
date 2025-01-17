from timer_wrapper import clock
import numpy as np

n=10**10
primes5mod6 = np.ones((n//6+1), dtype=bool)
primes1mod6 = np.ones((n//6+1), dtype=bool)
clock.start()
for i in range(1,int((n**0.5+1)/6)+1):
    # print(i)
    if primes5mod6[i]:
        # print("-1m6", 6*i*i, 6*i*i-2*i)
        primes5mod6[6*i*i::6*i-1]= False
        primes1mod6[6*i*i-2*i::6*i-1]= False
    if primes1mod6[i]:
        # print("1m6", 6*i*i, 6*i*i+2*i)
        primes5mod6[6*i*i::6*i+1]= False
        primes1mod6[6*i*i+2*i::6*i+1]= False
clock.stop()

# Take the wheel and multiply by x (one of the values of the wheel) under mod 30.
# The first value in the resulting vector that is equal to x will be the form of our starting value say 'a',
# We then need to find the smallest value of x 