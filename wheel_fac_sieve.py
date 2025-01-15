from timer_wrapper import clock
import numpy as np
clock.start()
n=10**9
primes5mod6 = np.ones((n//6+1), dtype=bool)
primes1mod6 = np.ones((n//6+1), dtype=bool)
for i in range(1,int((n**0.5+1)/6)+1):
    if primes5mod6[i]:
        primes5mod6[6*i*i::6*i-1]= False
        primes1mod6[6*i*i-2*i::6*i-1]= False
    if primes1mod6[i]:
        primes5mod6[6*i*i::6*i+1]= False
        primes1mod6[6*i*i+2*i::6*i+1]= False
clock.stop()