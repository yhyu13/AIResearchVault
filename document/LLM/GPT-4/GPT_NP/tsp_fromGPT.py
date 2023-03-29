from itertools import permutations

def travellingSalesmanProblem(graph, s):
    # Get number of vertices in the graph
    n = len(graph)
    
    # Create a list of all vertices except the starting vertex
    vertices = list(range(n))
    vertices.remove(s)
    
    # Create a list of all possible permutations of vertices
    perms = permutations(vertices)
    
    # Initialize minimum cost and minimum cost permutation
    min_cost = float('inf')
    min_perm = None
    
    # Loop through all permutations
    for perm in perms:
        # Add the starting vertex to the permutation
        perm = (s,) + perm
        
        # Calculate the cost of the permutation
        cost = 0
        for i in range(n):
            cost += graph[perm[i]][perm[(i+1)%n]]
        
        # Update minimum cost and minimum cost permutation if necessary
        if cost < min_cost:
            min_cost = cost
            min_perm = perm
    
    # Return minimum cost permutation
    return min_perm

if __name__ == "__main__":
 
    # matrix representation of graph
    graph = [[0, 10, 15, 20], [10, 0, 35, 25],
            [1, 35, 0, 30], [20, 25, 30, 0]]
    s = 0
    min_perm = travellingSalesmanProblem(graph, s)
    min_cost = sum(graph[min_perm[i]][min_perm[(i+1)%len(min_perm)]] for i in range(len(min_perm)))
    print(f"<answer>{min_cost}</answer>")