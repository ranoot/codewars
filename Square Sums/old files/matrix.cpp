#include <./matrix.hpp>
#include <iostream>
#include <vector>

template <typename T>
void print_matrix(matrix_vec<T> matrix) {
    for (auto it = matrix.begin(); it != matrix.end(); it++) {
        auto row = *it;
        for (auto jt = row.begin(); jt != row.end(); jt++) std::cout << *jt << " ";
        std::cout << "\n";
    }
}

template <typename T>
matrix_vec<T> init_matrix(size_t rows, size_t columns, T init_val) {
    std::vector<T> row(columns, init_val);
    matrix_vec<T> matrix(rows, row);
    return matrix;
}

template matrix_vec<bool> init_matrix(size_t rows, size_t columns, bool init_val);
template void print_matrix(matrix_vec<bool> matrix);