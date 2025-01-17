def path_finder(maze):
    working_nodes = [(len(maze) - 1, len(maze) - 1)]
    searched_nodes = set() # To take advantage of hashing
    #TODO: check if (n-1, n-1) is not a wall
    while len(working_nodes):
        for w_node in working_nodes:
            searched_nodes.add(w_node)
            working_nodes.remove(w_node)
            x, y = w_node
            for next_x, next_y in (x+1, y), (x-1, y), (x, y+1), (x, y-1):
                # print(next_node)
                if 0 <= next_x < len(maze) and 0 <= next_y < len(maze):
                    if maze[next_x][next_y] == 'W': continue 
                    if (next_x, next_y) in searched_nodes: continue
                    if (next_x, next_y) == (0,0): return True
                    working_nodes.append((next_x, next_y))
    return False
# very convoluted way of implementing DFS
maze = [
    "......",
    "......",
    "......",
    "......",
    ".....W",
    "....W."
]
print(path_finder(maze))