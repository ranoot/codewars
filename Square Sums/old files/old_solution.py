from math import isqrt
#* Tasks
# generate adjacency matrix
def gen_graph(num: int):
    possible_sq = [i*i for i in range(1, isqrt(2*num-1)+1)]
    # print(possible_sq)
    return [[(i + j in possible_sq) or i == 0 or j == 0 for j in range(num+1)] for i in range(num+1)] 

# backtrack a lot
# start from a universal vertex
# - check whether vertex was alr in path 
# - must be adjacent (an edge exists) to previous vertex
def find_path(graph, num, path: list) -> list|None: # 
    if len(path) == num + 1: # base case?
        # print("HELLO")
        return path 
    for v in range(1, num+1): 
        # print(path, v, graph[path[-1]][v], len(path))
        if (v not in path) and graph[path[-1]][v]:
            if (p:=find_path(graph, num, path + [v]))!=None:
                return p

NO_SOLN = set(range(2, 25)) - {15, 16, 17, 23}
def square_sums(num):
    if num in NO_SOLN:
        return False
    else:
        p = find_path(gen_graph(num), num, [0])
        return p[1:] if p != None else None