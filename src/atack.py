import random
import networkx as nx

def intact_nodes(G):
    return [n for n in G.nodes() if not G.nodes[n].get("failed", False)]


def random_node_attack(G0, number_of_nodes=1):
    G = G0.copy()
    intact = intact_nodes(G)
    failed_nodes = []

    for _ in range(min(number_of_nodes, len(intact))):
        node = random.choice(intact)
        G.remove_node(node)
        intact.remove(node)
        failed_nodes.append(node)

    return failed_nodes

# high degree node attack = high capacity node attack
def high_degree_node_attack(G0, number_of_nodes=1):
    G = G0.copy()
    intact = intact_nodes(G)

    node_degrees = {n: G.degree(n) for n in intact}
    sorted_nodes = sorted(node_degrees.items(), key=lambda x: x[1], reverse=True)

    failed_nodes = []
    for node, _ in sorted_nodes[:number_of_nodes]:
        G.remove_node(node)
        failed_nodes.append(node)

    return failed_nodes

# high betweenness node attack
def high_betweenness_node_attack(G, number_of_nodes=1, k=None):
    intact = intact_nodes(G)
    betweenness = nx.betweenness_centrality(G.subgraph(intact), normalized=True, k=k)
    failed_nodes = sorted(
        betweenness,
        key=betweenness.get,
        reverse=True
    )[:number_of_nodes]

    return failed_nodes

def high_load_node_attack(G0, number_of_nodes=1):
    G = G0.copy()
    intact = intact_nodes(G)

    node_loads = {n: G.nodes[n]['load'] for n in intact}
    sorted_nodes = sorted(node_loads.items(), key=lambda x: x[1], reverse=True)

    failed_nodes = []
    for node, _ in sorted_nodes[:number_of_nodes]:
        G.remove_node(node)
        failed_nodes.append(node)

    return failed_nodes

def high_load_capacity_ratio_node_attack(G0, number_of_nodes=1):
    G = G0.copy()
    intact = intact_nodes(G)

    node_ratios = {
        n: G.nodes[n]['load'] / G.nodes[n]['capacity']
        for n in intact
    }

    sorted_nodes = sorted(node_ratios.items(), key=lambda x: x[1], reverse=True)

    failed_nodes = []
    for node, _ in sorted_nodes[:number_of_nodes]:
        G.remove_node(node)
        failed_nodes.append(node)

    return failed_nodes

def high_load_capacity_ratio_and_degree_node_attack(G0, number_of_nodes=1):
    G = G0.copy()
    intact = intact_nodes(G)

    node_scores = {
        n: (G.nodes[n]['load'] / G.nodes[n]['capacity']) * G.degree(n)
        for n in intact
    }

    sorted_nodes = sorted(node_scores.items(), key=lambda x: x[1], reverse=True)

    failed_nodes = []
    for node, _ in sorted_nodes[:number_of_nodes]:
        G.remove_node(node)
        failed_nodes.append(node)

    return failed_nodes