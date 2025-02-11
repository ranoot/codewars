#include <vector>

template <typename T>
using matrix_vec = std::vector<std::vector<T>>;

template <typename T>
void print_matrix(matrix_vec<T> matrix);

template <typename T>
matrix_vec<T> init_matrix(size_t rows, size_t columns, T init_val);