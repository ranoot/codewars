#include <vector>
#include <deque>
#include <iostream>
#include <list>
#include <random>
#include <utility>
#include <algorithm>
#include <iterator>

struct shape_obj {
    unsigned int x_size;
    unsigned int y_size;
};

template <typename T>
using vec_iter = typename std::vector<T>::iterator;

template <typename T>
using const_vec_iter = typename std::vector<T>::const_iterator;

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

template <typename T>
std::pair< vec_iter<T>, vec_iter<T> > matrix<T>::row(unsigned int y) {
    auto start = data.begin() + y*x_size;

    return std::make_pair(start, start + x_size);
}

template <typename T>
const std::pair< const_vec_iter<T>, const_vec_iter<T> > matrix<T>::row(unsigned int y) const {
    const auto start = data.cbegin() + y*x_size;

    return std::make_pair(start, start + x_size);
}

void two_opt_swap(std::vector<int> &v, int v1, int v2) {
    std::reverse(v.begin() + (v1 + 1), v.begin() + v2 + 1);
}

auto calculate_cost_diff(const matrix<bool> &score_matrix, const std::vector<int> &v, int v1, int v2) {
    auto gain = score_matrix(v[v1],v[v2]) + score_matrix(v[v1+1],v[v2+1]);
    auto loss = score_matrix(v[v1],v[v1+1]) + score_matrix(v[v2], v[v2+1]);

    return gain - loss;
}

int compute_seq_score(const matrix<bool> &score_matrix, const std::vector<int> &v) {
    int score = 0;
    for (auto it = v.begin(); it!=(v.end()-1); it++) {
        score += (int)score_matrix(*it,*(it+1));
    }
    return score;
}

std::random_device dev;

typedef std::mt19937 MyRNG;
MyRNG rng(dev());

void get_sq_sum(const matrix<bool> &score_matrix, std::vector<int> &v) {
    const int n = v.size();
    std::uniform_int_distribution<int> n_rand_range(0, n-2); // endpoints are fixed
    for (int score = compute_seq_score(score_matrix, v); score < n-1;) {
        // Make v1 and v2 s.t. v1 < v2 and they are not the 2 end points and are minimally 2 apart
        int v2 = n_rand_range(rng);
        int v1 = n_rand_range(rng);
        while (abs(v1 - v2) <= 2) v1 = n_rand_range(rng);
        if (v1 > v2) std::swap(v1, v2);

        int delta = calculate_cost_diff(score_matrix, v, v1, v2);

        if (delta >= 0) {
            two_opt_swap(v, v1, v2);
            score += delta;
        }
    }
}


matrix<bool> gen_sq_sum_graph(int n) {
    matrix<bool> adj_matrix(n, n, false);
    int largest_square = n+n+1;
    for (int k = 2; k*k <= largest_square; k++) {
        int s = k*k;

        for (int i = 1; i<s and i<=n; i++) {
            if (i < s - n) {
                continue;
            }

            *adj_matrix(i-1,s-i-1) = true;
        }
    }
    return adj_matrix;
}

#define ITERATE_BACKWARDS
bool find_one_path(const matrix<bool> &adj_matrix, std::deque<int> &current_stack) {
    auto [x_size, _] = adj_matrix.shape();
    
    auto [row_iter, row_end_iter] = adj_matrix.row(current_stack.back());

    #ifdef ITERATE_BACKWARDS
    for (int i = x_size-1; i>=0; i--) {
        if (!row_iter[i]) continue;
    #else
    for (auto i = 0; i<x_size and row_iter!=row_end_iter; i++, row_iter++) {
        if (!(*row_iter)) continue;
    #endif

        if (i == current_stack.back()) continue;
        bool duplicate_el = false;
        for (const auto &vertex: current_stack) {
            if (i == vertex) {
                duplicate_el = true;
                goto skip;
            }
        }
        skip:
            if (duplicate_el) continue;

        current_stack.push_back(i);
        if (current_stack.size() < x_size) {
            if (find_one_path(adj_matrix, current_stack)) return true;
        } else { // we found a valid solution!
            return true; // pass a signal through all the functions that we succeeded!
        }
    }
    current_stack.pop_back(); // remove the element we are responsible for before returning
    return false;
}

std::vector<int> square_sums_row(int n)
{
    if (n < 25) {
        if(n==15 or n==16 or n==17 or n==23) {}
        else return std::vector<int> ();
    }

    auto sq_matrix = gen_sq_sum_graph(n);
    if (n < 35) {
        std::deque<int> stack2;
        for (int i = 0; i < n; i++) {
            stack2.push_back(i);
            if (find_one_path(sq_matrix, stack2)) {
                for (int &i: stack2) i++;
                return std::vector<int>(stack2.begin(), stack2.end());
            }
        }
    }

    std::vector<int> to_solve(n);

    to_solve[0] = 0;
    to_solve[to_solve.size()-1] = 2;
    std::iota(to_solve.begin()+1, to_solve.end()-1, 1);
    to_solve[2] = n-1;

    get_sq_sum(sq_matrix, to_solve);
    for (int &i: to_solve) i++;

    return to_solve;
}

int main() {
    auto to_solve = square_sums_row(15);
    for (const int &i: to_solve) std::cout << i << ", ";
    std::cout << "\n";
}