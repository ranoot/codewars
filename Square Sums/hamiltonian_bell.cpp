// Implementing bellman, held, karp algorithm in trying to find the hamiltonian path
#include <iostream>
#include <vector>
#include <array>
#include <cmath>

template <typename T>
using matrix_vec = std::vector<std::vector<T>>;

template <typename T>
void print_matrix(matrix_vec<T> matrix) {
    for (auto it = matrix.begin(); it != matrix.end(); it++) {
        auto row = *it;
        for (auto jt = row.begin(); jt != row.end(); jt++) std::cout << *jt << " ";
        std::cout << std::endl;
    }
}

template <typename T>
matrix_vec<T> init_matrix(size_t rows, size_t columns, T init_val) {
    std::vector<T> row(columns, init_val);
    matrix_vec<T> matrix(rows, row);
    return matrix;
}

matrix_vec<bool> gen_sq_sum_graph(int n) {   
    // TODO: Make an iterative version of this? 
    // very time consuming to keep computing this matrix, pattern is relatively simple

    auto adj_matrix = init_matrix(n, n, false);
    int largest_square = n+n+1;
    for (int k = 2; k*k <= largest_square; k++) {
        int s = k*k;
        std::cout << "square:" << s << std::endl;
        for (int i = 1; (i<s and i<=n); i++) {
            std::cout << i << std::endl;
            adj_matrix[i-1][s-i-1] = true;
        }
    }
    return adj_matrix;
}

matrix_vec<bool> gen_dp_matrix(matrix_vec<bool>& adj, int n) {
    matrix_vec<bool> dp_matrix {init_matrix(n, (1<<n), false)};
    
    for (int i = 0; i<n; i++) dp_matrix[i][2**i] = true; // subset with only i-th el will end with i-th el
    
    for (int i = 0; i<(1<<n); i++)
        for (int j = 0; j<n; j++)
            if (i&(1<<j)) { // j-th bit is set => j is in the mask i
                for (int k = 0; k<n; k++) { // look at all possible neighbours
                    if (k!=j and i&(1<<k) and adj[k][j]) { // k is in i, k and j are connected
                        if (dp_matrix[k][i^(1<<j)]) dp_matrix[j][i] = true;
                    }
                }
            }

    return dp_matrix;
}

std::vector<int> square_sum(int n);

void main() {

}