import copy

def cross(a: str, b: str):
    return [a_i + b_i for a_i in a for b_i in b]
    
digits = "123456789"
rows = "ABCDEFGHI"
cells = cross(rows, digits)

column_units = [cross(rows, i) for i in digits]
row_units = [cross(j, digits) for j in rows]
square_units = [cross(a, b) for a in ["ABC", "DEF", "GHI"] for b in ["123", "456", "789"]]
units = column_units + row_units + square_units

peers = {}
for identifier in cells:
    peers[identifier] = set([cell for unit in units if identifier in unit for cell in unit]) - {identifier}

class SudokuPuzzle:
    """Only contains 2 main fields, search_space and assigned_cells"""
    def __init__(self, puzzle, flattened = False):
        if not flattened:
            puzzle = [x for xs in puzzle for x in xs] #flatten

        self.search_space = self.init_search_space()
        self.assigned_cells = set()
        for cell, i in zip(cells, puzzle):
            if i != 0:
                # self.display_search_space()
                self.assign(cell, str(i))
        # print("done with init!")
                
    def init_search_space(self):
        return {cell: "123456789" for cell in cells}
    
    def assign(self, cell: str, i: str) -> bool:
        self.assigned_cells.add(cell)
        self.search_space[cell] = i

        to_be_assigned = []
        for peer in peers[cell]:
            peer_cell_value = self.search_space[peer]
            if len(peer_cell_value) >= 1: 
                self.search_space[peer] = peer_cell_value.replace(i, '')
                if len(self.search_space[peer]) == 0:
                    print("cell no option!")
                    return False
                if len(self.search_space[peer]) == 1 and peer not in self.assigned_cells:
                    if not self.assign(peer, self.search_space[peer]): return False
                    # to_be_assigned.append(peer)
            else: # our cell has no option anymore
                print("cell no option!")
                return False
        # for peer in to_be_assigned:
        #     if not self.assign(peer, self.search_space[peer]): return False
            
        return True
    
    def solved_puzzle(self):
        if len(self.assigned_cells) == 81:
            return [[int(self.search_space[row+column]) for column in digits] for row in rows]
        else:
            return False
        
    def display_search_space(self):
        output = "+-----------------------------+-----------------------------+-----------------------------+\n"
        line = "+-----------------------------+-----------------------------+-----------------------------+\n"
        for i, row_alphabet in enumerate(rows):
            row = [j for (cell, j) in self.search_space.items() if cell[0]==row_alphabet] #! should be sorted

            output += "|"
            for j in range(3):
                segment = row[3*j: 3*(j+1)]
                output += (" ".join([s.center(9) for s in segment]) + "|")
            output += "\n"
            if i%3 == 2:
                output += line
        print(output)

def solve_findall_helper(puzzle: SudokuPuzzle, solution_space: list[SudokuPuzzle]):
    if len(puzzle.assigned_cells) == 81:
        solution_space.append(puzzle)
        return
    # puzzle.display_search_space()
    # Not necessary but might be faster to find the smallest branches to start with
    cell, options = min(((cell, i) for cell, i in puzzle.search_space.items() if len(i) > 1), key = lambda x: len(x[1])) 
    for option in options:
        puzzle_copy = copy.deepcopy(puzzle) #TODO: Find a way to avoid all the deep copies
        if puzzle_copy.assign(cell, option):
            solve_findall_helper(puzzle_copy, solution_space)

def solve_findall(puzzle: SudokuPuzzle) -> list[SudokuPuzzle]:
    solution_space: list[SudokuPuzzle] = []

    solve_findall_helper(puzzle, solution_space)

    return solution_space
        
def sudoku(puzzle: list[list[int]]) -> list[list[int]]:
    if len(puzzle) != 9: raise Exception()
    for row in puzzle:
        if len(row) != 9: raise Exception()
        for cell_value in row:
            if not 0<=cell_value<=9: raise Exception()

    solved_puzzle_list = solve_findall(SudokuPuzzle(puzzle))

    if len(solved_puzzle_list) != 1: raise Exception()
    else: return solved_puzzle_list[0].solved_puzzle()

puzzle = [
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 1, 4, 0, 0, 0, 5, 8, 7],
    [0, 0, 7, 0, 0, 0, 0, 0, 0],
    [0, 8, 9, 0, 4, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 8, 0, 4, 5, 0],
    [0, 0, 0, 0, 0, 0, 2, 0, 0],
    [1, 5, 8, 0, 0, 0, 7, 3, 0],
    [0, 0, 0, 0, 0, 8, 9, 0, 0]
]

sudoku(puzzle)

# print(sum((1 for row in puzzle for cell_value in row if cell_value != 0)))