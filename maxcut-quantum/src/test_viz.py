from graph import generate_random_graph
from viz import draw_graph

n = 8
edges = generate_random_graph(n, edge_prob=0.4, seed=1)

print("Edges:", edges)

draw_graph(edges, n, title="Random Graph (Unweighted)", seed=2)