// find ninja pairs modulo 25
// Conditions
// 2 sequences: S and L or len n and (n+1) respectively.
// start with 1, end in (3 if odd len, 8 if even len)
// if i is in an odd position in S it must also be an odd position in L

#include <matrix.hpp>
#include <vector>
#include <deque>
#include <iostream>
#include <list>
#include <random>
#include <utility>
#include <algorithm>
#include <iterator>

// std::vector<int> test{0, 1, 2, 3, 4};
// auto test_iter = test.cbegin();
// auto test_span {std::span(test).subspan(0, 2)};

// try to compute ALL starting with 1 first
// then try to compute a ninja pair

matrix<bool> gen_sq_sum_graph(int n) {   
    // TODO: Make an iterative version of this? 
    // very time consuming to keep computing this matrix, pattern is relatively simple
    matrix<bool> adj_matrix(n, n, false);
    // adj_matrix.print();
    // std::cout << "INIT is fine!\n";
    int largest_square = n+n+1;
    for (int k = 2; k*k <= largest_square; k++) {
        int s = k*k;

        for (int i = 1; i<s and i<=n; i++) {
            if (i < s - n) {
                // printf("(%d, %d) ", i-1, s-i-1);
                continue;
            }
            // printf("(%d, %d) ", i-1, s-i-1);
            *adj_matrix(i-1,s-i-1) = true;
        }
        std::cout << "\n";
    }
    // std::cout << "generating the matrix is fine\n";
    return adj_matrix;
}

template <typename T>
void print_vector(const std::vector<T> &v) {
    for (const T &el: v) {
        std::cout << el << ", ";
    }
    std::cout << "\n";
}

template <typename T>
void print_queue(std::deque<T> &q) {
    for (const int &el: q) {
        std::cout << el << ", ";
    }
    std::cout << "\n";
}

void find_path_helper(const matrix<bool> &adj_matrix, std::deque<int> &current_stack) {
    auto [x_size, _] = adj_matrix.shape();
    
    auto [row_iter, row_end_iter] = adj_matrix.row(current_stack.back());
    for (auto i = 0; i<x_size and row_iter!=row_end_iter; i++, row_iter++) {
        if (!(*row_iter)) continue;
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
            // std::cout << current_stack.size() << std::endl;
            find_path_helper(adj_matrix, current_stack);
        } else { // we found a valid solution!
            std::cout << "FOUND!: ";
            print_queue<int>(current_stack);
            current_stack.pop_back();
        }
    }
    current_stack.pop_back(); // remove the element we are responsible for before returning
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

// void two_opt_swap(std::vector<int> &v, int v1, int v2) {
//     // v1 and v2 are the first vertices of the edges that are to be swapped when traversing through the route
//     std::deque<int> to_reverse;
//     for (auto i = v1+1; i<=v2; i++) to_reverse.push_back(v[i]);
//     for (auto i = v1+1; i<=v2; i++) {
//         // std::cout << to_reverse.back() << std::endl;
//         v[i] = to_reverse.back();
//         to_reverse.pop_back();
//     }
// }
void two_opt_swap(std::vector<int> &v, int v1, int v2) {
    std::reverse(v.begin() + (v1 + 1), v.begin() + v2 + 1);
}

auto calculate_cost_diff(const matrix<bool> &score_matrix, const std::vector<int> &v, int v1, int v2) {
    // v1 will be connected to v2
    // v1 + 1 will be connected to v2 + 1
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

const_vec_iter<int> find_non_compliant(const matrix<bool> &score_matrix, const std::vector<int> &v) {
    for (auto it = v.begin(); it!=(v.end()-1); it++) {
        if (!score_matrix(*it,*(it+1))) return it;
    }
    return v.end();
}

int find_non_compliant_index(const matrix<bool> &score_matrix, const std::vector<int> &v) {
    // returns the first non compliant index
    for (int i = 0; i<v.size()-1; i++) {
        if (!score_matrix(v[i], v[i+1])) return i;
    }
    return v.size();
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
        
        // if (score >= 98) {
        //     print_vector(v);
        //     auto nc = find_non_compliant(score_matrix, v);
        //     if (nc!=v.end()) std::cout << *nc << "\n";
        // }
        int delta = calculate_cost_diff(score_matrix, v, v1, v2);
        // printf("v1: %d, v2: %d, score=%d, actual_score=%d delta=%d\n", v1, v2, score, compute_seq_score(score_matrix, v), delta);

        if (delta >= 0) {
            // int initial_score = compute_seq_score(score_matrix, v);
            // printf("DELTA >= 0: \n");
            // printf("v1=%d v1+1=%d, v2=%d, v2+1=%d\n", v[v1], v[v1+1], v[v2], v[v2+1]);
            // printf("GAIN (v1, v2)=%d, (v1+1,v2+1)=%d\n", score_matrix(v[v1],v[v2]), score_matrix(v[v1+1],v[v2+1]));
            // printf("LOSS (v1, v1+1)=%d, (v2, v2+1)=%d\n", score_matrix(v[v1],v[v1+1]), score_matrix(v[v2], v[v2+1]));
            // std::vector init_v(v);
            two_opt_swap(v, v1, v2);
            // int final_score = compute_seq_score(score_matrix, v);
            // printf("calculated delta: %d, actual delta: %d\n", delta, (final_score - initial_score));
            

            // if (delta != (final_score - initial_score)) {
            //     std::cout << "Final: ";
            //     print_vector(v);
            //     std::cout << "Initial: ";
            //     print_vector(init_v);
            // }
            score += delta;
        }
    }
}

int main (int argc, char* argv[]) {
    const int n = atoi(argv[1]);
    auto sq_matrix = gen_sq_sum_graph(n);
    // sq_matrix.print();
    // auto [row_iter, row_end] = sq_matrix.row(1);
    // for (auto it = row_iter; it != row_end; it++) std::cout << *it << ", "; 
    // std::cout << "\n";

    //* testing find_path_helper
    // std::deque<int> stack;
    // stack.push_back(0);
    // find_path_helper(sq_matrix, stack);
    
    //* testing find_one_path
    // std::deque<int> stack2;
    // stack2.push_back(0);
    // find_one_path(sq_matrix, stack2);
    // print_queue(stack2);

    std::vector<int> to_solve(n);
    // our ninja sequences start with 1 and end with 3
    to_solve[0] = 0;
    to_solve[to_solve.size()-1] = 2;
    std::iota(to_solve.begin()+1, to_solve.end()-1, 1);
    to_solve[2] = n-1;
    
    get_sq_sum(sq_matrix, to_solve);

    print_vector<int>(to_solve);
    std::cout << "Score: " << compute_seq_score(sq_matrix, to_solve) << "\n";
    // sq_matrix.print();
}