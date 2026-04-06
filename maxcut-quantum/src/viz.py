import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(edges, n, title=None, seed=0):
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for u, v, w in edges:
        G.add_edge(u, v, weight = w)

    pos = nx.spring_layout(G, seed=seed)

    plt.figure()
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray"
    )

    if title:
        plt.title(title)

    plt.margins(0.1)
    plt.show()

def draw_cut(n, edges, bitstring, title = None, seed = 0):
    """
    Draw graph with cut visualization
    """
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for u, v, w in edges:
        G.add_edge(u, v, weight = w)

    pos = nx.spring_layout(G, seed = seed)

    # Color nodes by partition
    node_colors = ["blue" if bitstring[i] == 1 else "red" for i in range(n)]

    edge_colors = []
    edge_widths = []
    for u, v, w in edges:
        if bitstring[u] != bitstring[v]:
            edge_colors.append("green")
            edge_widths.append(2.5)
        else:
            edge_colors.append("gray")
            edge_widths.append(1.0)

    plt.figure()
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color = node_colors,
        edge_color = edge_colors,
        width = edge_widths,
        node_size = 800,
    )

    if title:
        plt.title(title)
    plt.margins(0.1)
    plt.show()