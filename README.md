# Codewars Repo
My solutions/ non-solutions (mostly non-solutions) to codewars problems

## Prime counting
Link: <https://www.codewars.com/kata/638c92b10e43cc000e615a07/train/python>

Includes many iterations of implementing prime sieves, Meissel-Lehmer algorithm (under `primes.py`), LMO (under `new_primes.py`)
The LMO implementation is based on [this paper](https://www.ams.org/journals/mcom/1985-44-170/S0025-5718-1985-0777285-5/S0025-5718-1985-0777285-5.pdf) but without all the segmentation implementations. 
Define a wrapper object with `class PrimeCounter(n)`, where n is the largest possible `.count(n)` you can compute with this object. A lot of caching is required so it gets faster the more times you call `.count(n)`

Performance for these are still unsatisfactory, but they are functional nonetheless (to the best of my knowledge). There is also a huge memory issue involved with computing the phi function, where we have to save each intermediate step of the SoE for every single prime. Other memory issues include the F_array and the phi_cache. This nearly fully used up my RAM after a lot of use.

### Computing $\phi(n)$
The only difficult part from the paper is computing the contributions of the special leaves $S_{2}(x, a)$
1. Sieve the block $[1, \lfloor x^{\frac{2}{3}} \rfloor]$, storing all the intermediate results.
2. Compute the array $\mathbf{F} = \{ (m, f(m), \mu(m)), m \in [1, \lfloor x^{\frac{1}{3}} \rfloor] \}$, where f computes the smallest prime factor (This can be computed during the sieving).
3. Now, for each prime $p_b \leq \lfloor x^{\frac{1}{3}} \rfloor$,
  - We look for the corresponding $f(m)$ such that $f(m) > p_b$ and $p_b*m > \lfloor x^{\frac{1}{3}} \rfloor$
  - We compute $\mu(m)\phi(\lfloor \frac{x}{p_b*m} \rfloor, b)$ using the intermediate sieving steps mentioned above. (The research paper mentions some other formula that I am unsure of how to use, and would have likely required the use of a segmented version of this computation. Which I am reluctant to implement.)
  - *Subtract* this computation from our accumulated $S_2$ value.
4. Return our accumulated $S_2$ value.

Further improvements:
- Improving prime sieve via wheel factorization.
- Implement the segmented version of the phi computation.
- Implement a segmented sieve (An attempt was made in one of the firsts commits to this repo).
- We just need to sieve up to 10^10 within 8s? Which we can precompute and compute `pi(n)` for any n <= 10^10.
