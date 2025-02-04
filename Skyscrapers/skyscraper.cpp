#include <array>

typedef std::array<std::array<std::array<bool, 4>, 4>, 4> soln_space_type;

soln_space_type init_soln_space() {
    // initialises the soln space based on the clues given
    // using the naive limitations due to the nature of the position of the tallest tower
    soln_space_type soln_space;
    for (int i = 0; i<4; i++) 
        for (int j = 0; j<4; j++) 
            for (int k = 0; k<4; k++) 
                soln_space[i][j][k] = true;
}

int** solve_puzzle(int* clues) {
    
}