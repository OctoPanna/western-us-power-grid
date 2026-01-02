#--------------------------------------------------
# As you can't import functions from jupyter notebook, I copied it here
# --------------------------------------------------

import networkx as nx
import numpy as np

from cascade_failure.updated_model import load_data


# --------------------------------------------------
# Betweenness-based load and capacity initialization
# --------------------------------------------------
def initialize_betweenness_loads(G, alpha=0.2):
    bet = nx.betweenness_centrality(G, normalized=True)
    for n in G.nodes():
        G.nodes[n]["load"] = bet[n]
        G.nodes[n]["capacity"] = (1 + alpha) * bet[n]
        G.nodes[n]["failed"] = False


# --------------------------------------------------
# Cascading failure simulation
# --------------------------------------------------
def cascade_failure(G, initial_attack=None, alpha=0.2, verbose=False):
    G = G.copy()
    initialize_betweenness_loads(G, alpha)

    failed_nodes = set()
    step = 0

    # Initial attack
    if initial_attack is not None:
        G.remove_node(initial_attack)
        failed_nodes.add(initial_attack)

    while True:
        step += 1
        bet = nx.betweenness_centrality(G, normalized=True)

        newly_failed = []
        for n in G.nodes():
            load = bet[n]
            capacity = G.nodes[n]["capacity"]
            if load > capacity:
                newly_failed.append(n)

        if not newly_failed:
            break

        if verbose:
            print(f"Step {step}: {len(newly_failed)} new failures")

        for n in newly_failed:
            G.remove_node(n)
            failed_nodes.add(n)

    # Metrics
    if G.number_of_nodes() > 0:
        largest_cc = len(max(nx.connected_components(G), key=len))
    else:
        largest_cc = 0

    return {
    "failed_nodes": failed_nodes,
    "num_failed": len(failed_nodes),
    "largest_cc": largest_cc,
    "remaining_nodes": G.number_of_nodes(),
    "steps": step,
    "final_graph": G}

