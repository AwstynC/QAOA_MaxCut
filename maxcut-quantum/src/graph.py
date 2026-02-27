import random

def generate_random_graph(n, edge_prob=0.5, seed=None):
    """
    Generate unweighted undirected random graph.
    Returns list of edges: [(u, v), ...]
    """
    if seed is not None:
        random.seed(seed)

    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < edge_prob:
                edges.append((i, j))
    return edges


def cut_value(bitstring, edges):
    total = 0
    for u, v in edges:
        if bitstring[u] != bitstring[v]:
            total += 1
    return total


def int_to_bitlist(x, n):
    return [(x >> i) & 1 for i in range(n)]


def cut_value(bitstring, edges):
    """
    Compute cut value for a given bitstring.
    bitstring: list of 0/1 ints
    edges: [(u, v, w)]
    """
    total = 0
    for u, v, w in edges:
        if bitstring[u] != bitstring[v]:
            total += w
    return total


def int_to_bitlist(x, n):
    return [(x >> i) & 1 for i in range(n)]