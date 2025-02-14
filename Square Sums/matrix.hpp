#include <vector>
// #include <span>
#include <iostream>

// template <typename T>
// using matrix_vec = std::vector< std::vector<T> >;

// template <typename T>
// void print_matrix(matrix_vec<T> matrix);

// template <typename T>
// matrix_vec<T> init_matrix(size_t rows, size_t columns, T init_val);

struct shape_obj {
    unsigned int x_size;
    unsigned int y_size;
};

template <typename T>
using vec_iter = std::vector<T>::iterator;

template <typename T>
using const_vec_iter = std::vector<T>::const_iterator;

template <typename T>
class matrix {
        std::vector<T> data; 
        unsigned int x_size;
        unsigned int y_size;
    public:
        matrix(int r, int c, T init_value);

        const shape_obj shape() const;

        const T operator()(unsigned int i, unsigned int j) const;
        vec_iter<T> operator()(unsigned int i, unsigned int j);

        std::pair< vec_iter<T>, vec_iter<T> > row(unsigned int y);
        const std::pair< const_vec_iter<T>, const_vec_iter<T> > row(unsigned int y) const;
        
        void print() const;
};

template <typename T>
matrix<T>::matrix(int x, int y, T init_value) {
    data = std::vector<T>(x*y, init_value);
    x_size = x;
    y_size = y;
}

template <typename T>
const shape_obj matrix<T>::shape() const { 
    shape_obj s{x_size, y_size}; 
    return s;
}

template <typename T>
vec_iter<T> matrix<T>::operator()(unsigned int i, unsigned int j) {
    return data.begin() + i + x_size*j;
}

template <typename T>
const T matrix<T>::operator()(unsigned int i, unsigned int j) const {
    return data[i + x_size*j];
}

// template <typename T> 
// const std::span<T>& matrix<T>::row(unsigned int y) const {
//     return std::span<T> {data.begin() + y*x_size, x_size};
// }

template <typename T>
std::pair< vec_iter<T>, vec_iter<T> > matrix<T>::row(unsigned int y) {
    // auto start = y*x_size;
    // return std::span(data).subspan(start, start + x_size);

    auto start = data.begin() + y*x_size;
    // return std::ranges::subrange<T> {start, start + x_size};

    return std::make_pair(start, start + x_size);
}

template <typename T>
const std::pair< const_vec_iter<T>, const_vec_iter<T> > matrix<T>::row(unsigned int y) const {
    const auto start = data.cbegin() + y*x_size;

    return std::make_pair(start, start + x_size);
}

template <typename T>
void matrix<T>::print() const {
    std::cout << data.size() << "\n";
    for (int y = 0; y<y_size; y++) {
        auto [row_iter, row_end] = row(y);
        // std::cout << y << ": ";
        for (auto it = row_iter; it != row_end; it++) {
            // std::cout << *it << " ";
            std::cout << *it;
        }
        std::cout << "\n";
    }
}