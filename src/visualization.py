import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(G):
    plt.figure(figsize=(10, 8))

    pos = nx.get_node_attributes(G, "pos")

    nx.draw(
        G,
        pos,
        node_color="#50bee6",
        node_size=3,
        edge_color="grey",
    )

    plt.title("Network Graph")
    plt.show()

def draw_graph_after_failure(G_before, failed_edges):
    pos = nx.get_node_attributes(G_before, "pos")

    plt.figure(figsize=(10, 8))

    intact_edges = [e for e in G_before.edges() if e not in failed_edges and (e[1], e[0]) not in failed_edges]
    nx.draw_networkx_edges(G_before, pos, edgelist=intact_edges, edge_color='grey', alpha=0.7)

    nx.draw_networkx_edges(G_before, pos, edgelist=failed_edges, edge_color='red', alpha=0.9)

    failed_nodes = set()
    for u, v in failed_edges:
        failed_nodes.add(u)
        failed_nodes.add(v)
    node_colors = ["#9c0101" if n in failed_nodes else "#50bee6" for n in G_before.nodes()]
    nx.draw_networkx_nodes(G_before, pos, node_color=node_colors, node_size=3)

    plt.title("Network Graph After Cascade Failure")
    plt.axis('off')
    plt.show()