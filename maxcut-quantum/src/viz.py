import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(edges, n, title=None, seed=0):
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)

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

    plt.tight_layout()
    plt.show()