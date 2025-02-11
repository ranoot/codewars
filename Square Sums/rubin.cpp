#include "matrix.h"
#include <iostream>

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

int main() {
    matrix_vec<bool> adj_matrix = gen_sq_sum_graph(50);
    for (const auto row: adj_matrix) {
        int i = 0;
        for (const auto v: row) {
            if (v) i++;
        }
        std::cout << i << std::endl;
    }
}