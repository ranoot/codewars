#include <./matrix.hpp>
#include <iostream>
#include <vector>

matrix_vec<bool> gen_sq_sum_graph(int n) {   
    // TODO: Make an iterative version of this? 
    // very time consuming to keep computing this matrix, pattern is relatively simple
    auto adj_matrix = init_matrix<bool>(n, n, false);
    int largest_square = n+n+1;
    for (int k = 2; k*k <= largest_square; k++) {
        int s = k*k;
        // std::cout << "square:" << s << std::endl;
        for (int i = 1; (i<s && i<=n); i++) {
            // std::cout << i << std::endl;
            adj_matrix[i-1][s-i-1] = true;
        }
    }
    return adj_matrix;
}

int main() {
    matrix_vec<bool> adj_matrix = gen_sq_sum_graph(50);
    for (auto j = 0; j<adj_matrix.size(); j++) {
        int i = 0;
        for (const auto v: adj_matrix[j]) {
            if (v) i++;
        }
        std::cout << j << " " << i << std::endl;
    }
    print_matrix(adj_matrix);
}