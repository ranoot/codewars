// Implementing bellman, held, karp algorithm in trying to find the hamiltonian path
#include "matrix.h"
#include <iostream>
#include <vector>
#include <array>
#include <cmath>

// template <typename T>
// using matrix_vec = std::vector<std::vector<T>>;

matrix_vec<bool> gen_sq_sum_graph(int n) {   
    // TODO: Make an iterative version of this? 
    // very time consuming to keep computing this matrix, pattern is relatively simple

    auto adj_matrix = init_matrix(n, n, false);
    int largest_square = n+n+1;
    for (int k = 2; k*k <= largest_square; k++) {
        int s = k*k;
        // std::cout << "square:" << s << std::endl;
        for (int i = 1; (i<s && i<=n); i++) {
            std::cout << i << std::endl;
            adj_matrix[i-1][s-i-1] = true;
        }
    }
    return adj_matrix;
}

matrix_vec<bool> gen_dp_matrix(matrix_vec<bool>& adj, int n) {
    matrix_vec<bool> dp_matrix {init_matrix(n, (1<<n), false)};
    
    for (int i = 0; i<n; i++) dp_matrix[i][1<<i] = true; // subset with only i-th el will end with i-th el
    
    for (int i = 0; i<(1<<n); i++)
        for (int j = 0; j<n; j++)
            if (i&(1<<j)) { // j-th bit is set => j is in the mask i
                for (int k = 0; k<n; k++) { // look at all possible neighbours
                    if (k!=j && i&(1<<k) && adj[k][j]) { // k is in i, k and j are connected
                        if (dp_matrix[k][i^(1<<j)]) dp_matrix[j][i] = true;
                    }
                }
            }

    return dp_matrix;
}

std::vector<int> square_sum(int n);

int main() {
    matrix_vec<bool> adj_matrix {gen_sq_sum_graph(17)};
    matrix_vec<bool> dp_matrix {gen_dp_matrix(adj_matrix, 17)};
    for (int i = 0; i<15; i++) std::cout << dp_matrix[i][dp_matrix.size()-1] << std::endl;
    // print_matrix(dp_matrix);
}