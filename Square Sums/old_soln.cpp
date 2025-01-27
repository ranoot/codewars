#include <vector>
#include <algorithm>
#include <iostream>

// we check vertex from 0 to n-1
// path must be non-empty, include element to start with
std::vector<int> find_path(std::vector<std::vector<bool>> &adj, int n, std::vector<int> &path) {
    if (path.size() == n) return path;
    for (int v = 0; v < n; v++) {
        if (std::find(path.begin(), path.end(), v) == path.end() && adj[v][path.back()]) {
            path.push_back(v);
            return find_path(adj, n, path);
        }
    }
}

int main() {
    std::cout << "Hello World!" << std::endl;
    return 1;
}