"""
https://www.geeksforgeeks.org/print-all-hamiltonian-cycles-in-an-undirected-graph/

# This code is contributed by divyesh072019.
"""


def is_safe(v, graph, path, pos):
    """
    Function to check if a vertex v can be added at index pos in the
    Hamiltonian Cycle
    """
    # If the vertex is adjacent to the vertex of the previously added vertex
    if graph[path[pos - 1]][v] == 0:
        return False

    # If the vertex has already been included in the path
    for i in range(pos):
        if path[i] == v:
            return False

    # Both the above conditions are not true, return true
    return True


# To check if there exists at least 1 hamiltonian cycle
hasCycle = False


def hamiltonian_cycle(graph):
    """
    Function to find all possible hamiltonian cycles.
    """
    global hasCycle

    # Initially value of boolean flag is false
    hasCycle = False

    # Store the resultant path
    path = [0]

    # Keeps the track of the visited vertices
    visited = [False] * (len(graph))

    for i in range(len(visited)):
        visited[i] = False

    visited[0] = True

    # Prepare a file in which we will save Hamiltonian path data.
    import pathlib
    out_dir = str(pathlib.Path().resolve().parent.resolve()) + "\\data"
    out_file = out_dir + "\\hamiltonian_cycles_temp.txt"
    open(out_file, 'w+').close()
    f = open(out_file, 'a+')

    # Function call to find all hamiltonian cycles
    find_hamiltonian_cycles(graph, 1, path, visited, out_file, f)
    f.close()

    if hasCycle:
        # If no Hamiltonian Cycle is possible for the given graph
        print("No Hamiltonian Cycle" + "possible ")
        return


def find_hamiltonian_cycles(graph, pos, path, visited, out_file, f):
    """
    Recursive function to find all hamiltonian cycles.
    """

    # If all vertices are included in Hamiltonian Cycle.
    if pos == len(graph):

        # If there is an edge from the last vertex to the source vertex.
        if graph[path[-1]][path[0]] != 0:

            # Include source vertex into the path and print the path.
            path.append(0)
            for i in range(len(path)):
                print(path[i], end=" ", file=f)
            print(file=f)

            # Remove the source vertex added.
            path.pop()

            # Update the hasCycle as true
            hasCycle = True
        return

    # Try different vertices as the next vertex
    for v in range(len(graph)):

        # Check if this vertex can be added to Cycle
        if is_safe(v, graph, path, pos) and not visited[v]:
            path.append(v)
            visited[v] = True

            # Recur to construct rest of the path
            find_hamiltonian_cycles(graph, pos + 1, path, visited, out_file, f)

            # Remove current vertex from path and process other vertices
            visited[v] = False
            path.pop()


if __name__ == "__main__":
    graph = [
        [0, 1, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 1],
        [1, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1],
        [1, 1, 0, 0, 1, 0],
    ]
    hamiltonian_cycle(graph)
