#include <matrix.hpp>
#include <vector>
#include <iostream>
#include <list>
#include <random>
#include <utility>
#include <algorithm>
#include <iterator>
#include <memory>

class node {
    public:
        node(int d): data{ d } {}
        std::shared_ptr<node> next;
        std::shared_ptr<node> prev;
        int data;
};

auto init_path(const std::vector<int> &v) {
    std::shared_ptr<node> start_node { new node{ v[0] } };
    std::shared_ptr<node> prev_node = start_node;
    for (auto it = v.begin()+1; it!=v.end(); it++) {
        prev_node->next = std::shared_ptr<node>(new node{ *it });
        prev_node->next->prev = prev_node;
        prev_node = prev_node->next;
    }
    start_node->prev = prev_node;
    prev_node-> next = start_node;
    return start_node;
}

void print_path(std::shared_ptr<node> start) {
    auto curr_node = start;
    do {
        std::cout << curr_node->data << ", ";
        curr_node = curr_node->next;
    } while (curr_node != start);
    std::cout << "\n";
}

auto push_ptr(std::shared_ptr<node> ptr, int i) {
    auto curr_ptr = ptr;
    for (int k = 0; k < i; k++) {
        curr_ptr = curr_ptr->next;
    }
    return curr_ptr;
}

void three_opt_swap(std::shared_ptr<node> start_ptr, int v1, int v2, int v3, int option) {
    if (option==0) return;
    // Assume that v1 < v2 < v3
    auto fst_node = push_ptr(start_ptr, v1); //1<->2
    auto snd_node = push_ptr(fst_node, v2-v1);
    auto trd_node = push_ptr(snd_node, v3-v2);

    switch (option) {
        case 1: //reverse 1<->2
            
            break;
    }
}

int main() {
    auto start_node = init_path(std::vector<int>{ 1, 2, 3, 4 });
    printf("We initialised! %d %d\n", start_node->data, start_node->next->data);
    print_path(start_node);
}