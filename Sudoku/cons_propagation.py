import traceback
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
    
    def assign(self, cell: str, i: str) -> bool:
        self.assigned_cells.add(cell)
        self.search_space[cell] = i

        # to_be_assigned = []
        for peer in peers[cell]:
            peer_cell_value = self.search_space[peer]
            if len(peer_cell_value) >= 1: 
                self.search_space[peer] = peer_cell_value.replace(i, '')
                if len(self.search_space[peer]) == 0:
                    # print("cell no option!")
                    return False
                if len(self.search_space[peer]) == 1 and peer not in self.assigned_cells:
                    if not self.assign(peer, self.search_space[peer]): return False
                    # to_be_assigned.append(peer)
            else: # our cell has no option anymore
                # print("cell no option!")
                return False
        # for peer in to_be_assigned:
        #     if not self.assign(peer, self.search_space[peer]): return False
            
        return True
    
    def solved_puzzle(self):
        if len(self.assigned_cells) == 81:
            return [[int(self.search_space[row+column]) for column in digits] for row in rows]
        else:
            return False

def nine_by_nine_format(puzzle):
        output = "+-----+-----+-----+\n"
        line = "+-----+-----+-----+\n"
        for i in range(9):
            row = puzzle[9*i: 9*(i+1)]
            output += "|"
            for j in range(3):
                segment = row[3*j: 3*(j+1)]
                output += (" ".join([str(s) for s in segment]) + "|")
            output += "\n"
            if i%3 == 2:
                output += line
        return output

def solve(puzzle: SudokuPuzzle) -> SudokuPuzzle|None: # We try to use recursive DFS
    if len(puzzle.assigned_cells) == 81:
        return puzzle

    # Not necessary but might be faster to find the smallest branches to start with
    cell, options = min(((cell, i) for cell, i in puzzle.search_space.items() if len(i) > 1), key = lambda x: len(x[1])) 

    for option in options:
        puzzle_copy = copy.deepcopy(puzzle) #TODO: Find a way to avoid all the deep copies
        if puzzle_copy.assign(cell, option):
            output = solve(puzzle_copy)
            if output != None: return output 

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


assert peers['A1'] == set([
    'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', # same column
    'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', # same row
    'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'  # same box
])

# print(square_units)

for cell in cells:
    assert len(peers[cell]) == 20

puzzle = SudokuPuzzle([
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 1, 4, 0, 0, 0, 5, 8, 7],
    [0, 0, 7, 0, 0, 0, 0, 0, 0],
    [0, 8, 9, 0, 4, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 8, 0, 4, 5, 0],
    [0, 0, 0, 0, 0, 0, 2, 0, 0],
    [1, 5, 8, 0, 0, 0, 7, 3, 0],
    [0, 0, 0, 0, 0, 8, 9, 0, 0]
])

print(len(solve_findall(puzzle)))

# assert solve(SudokuPuzzle([
#     [5, 3, 0, 0, 7, 0, 0, 0, 0], 
#     [6, 0, 0, 1, 9, 5, 0, 0, 0], 
#     [0, 9, 8, 0, 0, 0, 0, 6, 0], 
#     [8, 0, 0, 0, 6, 0, 0, 0, 3], 
#     [4, 0, 0, 8, 0, 3, 0, 0, 1], 
#     [7, 0, 0, 0, 2, 0, 0, 0, 6], 
#     [0, 6, 0, 0, 0, 0, 2, 8, 0], 
#     [0, 0, 0, 4, 1, 9, 0, 0, 5], 
#     [0, 0, 0, 0, 8, 0, 0, 7, 9]
# ])).solved_puzzle() == [
#     [5, 3, 4, 6, 7, 8, 9, 1, 2], 
#     [6, 7, 2, 1, 9, 5, 3, 4, 8], 
#     [1, 9, 8, 3, 4, 2, 5, 6, 7], 
#     [8, 5, 9, 7, 6, 1, 4, 2, 3], 
#     [4, 2, 6, 8, 5, 3, 7, 9, 1], 
#     [7, 1, 3, 9, 2, 4, 8, 5, 6], 
#     [9, 6, 1, 5, 3, 7, 2, 8, 4], 
#     [2, 8, 7, 4, 1, 9, 6, 3, 5], 
#     [3, 4, 5, 2, 8, 6, 1, 7, 9]
# ]

# [
#     [3, 4, 6, 1, 2, 7, 9, 5, 8], 
#     [7, 8, 5, 6, 9, 4, 1, 3, 2], 
#     [2, 1, 9, 3, 8, 5, 4, 6, 7], 
#     [4, 6, 2, 5, 3, 1, 8, 7, 9], 
#     [9, 3, 1, 2, 7, 8, 6, 4, 5], 
#     [8, 5, 7, 9, 4, 6, 2, 1, 3], 
#     [5, 9, 8, 4, 1, 3, 7, 2, 6],
#     [6, 2, 4, 7, 5, 9, 3, 8, 1],
#     [1, 7, 3, 8, 6, 2, 5, 9, 4]
# ]