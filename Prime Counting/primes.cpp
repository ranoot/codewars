#include <cmath>
// #include <iostream>

bool* prime_sieve(int n) {
    bool marks[n-1];
    // initialize all to true
    for (int i=0; i < n-1; i++) marks[i] = true;

    int limit{std::ceil(std::sqrt(n))};
    for (int i=0; i < limit; i++) {
        if (marks[i]) {
            int prime = i + 2;
            for (int j = (prime)*(prime) - 2; j < n-1; j += (prime)) {
                marks[j] = false;
            }
        }
    }
    return marks;
}

int main() {
    bool bool_arr[]{prime_sieve((int)std::pow(10, 10))};

    // for (bool b: bool_arr) {
    //     std::cout << b << std::endl;
    // }
}