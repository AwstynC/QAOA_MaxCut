from graph import generate_random_graph, cut_value

n = 5
edges = generate_random_graph(n, edge_prob=0.5, seed=1)

print("Edges:", edges)

bits = [0, 1, 0, 1, 0]
print("Cut value:", cut_value(bits, edges))