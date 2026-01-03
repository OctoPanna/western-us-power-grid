import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(G):
    plt.figure(figsize=(10, 8))

    pos = nx.get_node_attributes(G, "pos")

    nx.draw(
        G,
        pos,
        node_color="#ffc62a",
        node_size=3,
        edge_color="grey",
    )

    plt.title("Network Graph")
    plt.show()

# def draw_graph_after_failure(G_before, G_after, failed_edges, title):
#     pos = nx.get_node_attributes(G_before, "pos")

#     plt.figure(figsize=(10, 8))

#     intact_edges = [e for e in G_before.edges() if e not in failed_edges and (e[1], e[0]) not in failed_edges]
#     nx.draw_networkx_edges(G_before, pos, edgelist=intact_edges, edge_color='grey', alpha=0.7)

#     nx.draw_networkx_edges(G_before, pos, edgelist=failed_edges, edge_color='red', alpha=0.9)

#     failed_nodes = set()
#     for u, v in failed_edges:
#         edges_u = G_after.edges(u)
#         edges_v = G_after.edges(v)
#         if len(list(edges_u)) == 0:
#             failed_nodes.add(u)
#         if len(list(edges_v)) == 0:
#             failed_nodes.add(v)
#     node_colors = ["#9c0101" if n in failed_nodes else "#50bee6" for n in G_before.nodes()]
#     nx.draw_networkx_nodes(G_before, pos, node_color=node_colors, node_size=3)

#     plt.title(title)
#     plt.axis('off')
#     plt.show()

def draw_graph_after_failure(G, title):
    pos = nx.get_node_attributes(G, "pos")

    plt.figure(figsize=(10, 8))

    failed_edges = []
    intact_edges = []
    for u, v in G.edges():
        if G.nodes[u]["failed"] and G.nodes[v]["failed"]:
            failed_edges.append((u, v))
        else:
            intact_edges.append((u, v))

    nx.draw_networkx_edges(G, pos, edgelist=intact_edges, edge_color='grey', alpha=0.7)

    nx.draw_networkx_edges(G, pos, edgelist=failed_edges, edge_color='red', alpha=0.7)

    node_colors = ["#9c0101" if G.nodes[n]["failed"] else "#ffc62a" for n in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=3)

    plt.title(title)
    plt.axis('off')
    plt.show()

def draw_graph_with_node_highlighted(G, node_to_highlight, title="Network Graph with Highlighted Nodes"):
    plt.figure(figsize=(10, 8))

    pos = nx.get_node_attributes(G, "pos")

    node_colors = ['black' if node in node_to_highlight else '#ffc62a' for node in G.nodes()]

    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='grey', alpha=0.7)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=3)

    plt.title(title)
    plt.axis('off')
    plt.show()

def draw_graph_after_failure_with_attacked_nodes(G, attacked_nodes, title):
    pos = nx.get_node_attributes(G, "pos")

    plt.figure(figsize=(10, 8))

    failed_edges = []
    intact_edges = []
    for u, v in G.edges():
        if G.nodes[u]["failed"] and G.nodes[v]["failed"]:
            failed_edges.append((u, v))
        else:
            intact_edges.append((u, v))

    nx.draw_networkx_edges(G, pos, edgelist=intact_edges, edge_color='grey', alpha=0.7)

    nx.draw_networkx_edges(G, pos, edgelist=failed_edges, edge_color='red', alpha=0.7)

    node_colors = ["#051afc" if n in attacked_nodes else "#db0202" if G.nodes[n]["failed"] else "#ffc62a" for n in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=3)

    plt.title(title)
    plt.legend(handles=[
        plt.Line2D([0], [0], marker='o', color='w', label='Attacked Nodes', markerfacecolor='#051afc', markersize=8),
        plt.Line2D([0], [0], marker='o', color='w', label='Failed Nodes', markerfacecolor='#db0202', markersize=8),
        plt.Line2D([0], [0], marker='o', color='w', label='Intact Nodes', markerfacecolor='#ffc62a', markersize=8)
    ], loc='lower right')
    plt.axis('off')
    plt.show()