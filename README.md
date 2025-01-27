# Codewars Repo
My solutions/ non-solutions (mostly non-solutions) to codewars problems

## Prime counting
Link: <https://www.codewars.com/kata/638c92b10e43cc000e615a07/train/python>

Includes many iterations of implementing prime sieves, Meissel-Lehmer algorithm (under `primes.py`), LMO (under `new_primes.py`)

Define a wrapper object with `class PrimeCounter(n)`, where n is the largest possible `.count(n)` you can compute with this object. A lot of caching is required so it gets faster the more times you call `.count(n)`

Performance for these are still unsatisfactory, but they are functional nonetheless (to the best of my knowledge). 

### `new_primes.py` - LMO implementation

The LMO implementation is based on [this paper](https://www.ams.org/journals/mcom/1985-44-170/S0025-5718-1985-0777285-5/S0025-5718-1985-0777285-5.pdf) but without all the segmentation implementations. 

Most of the details of what is being computed can be found in the paper above. There is a huge memory issue involved with computing the phi function, where we have to save each intermediate step of the SoE for every single prime. Other memory issues include the F_array and the phi_cache. This nearly fully used up my RAM after a lot of use.

#### Computing $\phi(x, a)$
The only difficult part from the paper is computing the contributions of the special leaves $S_{2}(x, a)$
1. Sieve the block $[1, \lfloor x^{\frac{2}{3}} \rfloor]$, storing all the intermediate results.
2. Compute the array $\mathbf{F} = \\{ (m, f(m), \mu(m)), m \in [1, \lfloor x^{\frac{1}{3}} \rfloor] \\}$, where f computes the smallest prime factor (This can be computed during the sieving).
3. Now, for each prime $p_b \leq \lfloor x^{\frac{1}{3}} \rfloor$,
  - We look for the corresponding $f(m)$ such that $f(m) > p_b$ and $p_b*m > \lfloor x^{\frac{1}{3}} \rfloor$
  - We compute $\mu(m)\phi(\lfloor \frac{x}{p_b*m} \rfloor, b)$ using the intermediate sieving steps mentioned above. (The research paper mentions some other formula that I am unsure of how to use, and would have likely required the use of a segmented version of this computation. Which I am reluctant to implement.)
  - **Subtract** this computation from our accumulated $S_2$ value.
4. Return our accumulated $S_2$ value.

#### Some optimisations that I have tried

- Wherever possible, I have tried to use numpy functions as they are generally faster. Made use of funtions like `np.count_nonzero()` (which is faster than `np.sum`) and `np.search_sorted()` where applicable.
- Memoization implemented for the naive phi function to reduce the number of `np.count_zero()`. Used bisect to search through the sorted phi_cache, which has to be a list since its elements must be dynamically allocated. Its elements are then inserted in order to preserve the ordering.
- Pre-ordering of the **F** array. When using the sieve to compute this array, the m values will not be inserted in order. We pre-sort the array so that we can avoid enumerating through the entire F array, which will be very costly as **F** is precomputed for the computation of $10^{10}$.

### Prime Sieve optimized via wheel factorization

Implementation mostly by user14042 on [this Math StackExchange article](https://math.stackexchange.com/questions/3777437/how-can-wheel-factorization-be-used-to-speed-up-sieving)

Under `prime_test.ipynb`, we compute the "offset" for the starting values of each combination of row and modulo_wheel (we call this $k$)

#### Computing offsets, then computing the associated index
We first take the "row" that we want to compute offset_values for (corresponding to a certain value in our wheel),
Then for each possible type of prime, call this $p_{mod}$(which is represented by our wheel) which corresponds to each row in the column matrix, 
Find the value which equals our "row" then get the corresponding wheel number of the column, call this $m$
Then compute the offset, by taking $m' - p_{mod}'$ (m' and p_mod' corresponds to the prime modulo that works for each row)

To compute the index, we need to solve: $30i' + \alpha = p(p+k), p = 30i + \beta$ where k is our offset $\alpha$ and $\beta$ must be in "indexable" form. $\alpha$ is our row value and $\beta$ is just our prime modulo.

Further improvements:
- Improving prime sieve via wheel factorization.
- Implement the segmented version of the phi computation.
- Implement a segmented sieve (An attempt was made in one of the firsts commits to this repo).
- We just need to sieve up to 10^10 within 8s? Which we can precompute and compute `pi(n)` for any $n \leq 10^{10}$.

## Path Finding

`paths.py` contains a rather convoluted way of implementing DFS.

## Sudoku Solver

Link (3 kyu): <https://www.codewars.com/kata/sudoku-solver/python>
Link (2 kyu): <https://www.codewars.com/kata/5588bd9f28dbb06f43000085>

File `Sudoku/`, contains implementation of sudoku solvers using constraint propagation and some backtracking (using recursive DFS).
