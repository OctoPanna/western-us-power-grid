import networkx as nx

def cascade_failure_equal_load_distribution(G0, failed_nodes0):
    G = G0.copy()

    current_failed = list(failed_nodes0)
    failed_per_step = []
    steps = 0

    while current_failed:
        steps += 1
        new_failed = set()

        for n in current_failed:
            if G.nodes[n]["failed"]:
                continue

            G.nodes[n]["failed"] = True
            neighbors = get_intack_neighbours(G, n)
            load = G.nodes[n]["load"]

            if neighbors:
                load_per_neighbor = load / len(neighbors)
                for neighbor in neighbors:
                    G.nodes[neighbor]["load"] += load_per_neighbor
                    if G.nodes[neighbor]["load"] > G.nodes[neighbor]["capacity"]:
                        new_failed.add(neighbor)

            G.nodes[n]["load"] = 0  # prevent double redistribution

        failed_per_step.append(len(new_failed))
        current_failed = list(new_failed)

    outputs = calculate_outputs(G)
    return G, steps, failed_per_step, outputs

def cascade_failure_proportional_load_distribution(G0, failed_nodes0):
    G = G0.copy()

    current_failed = list(failed_nodes0)
    failed_per_step = []
    steps = 0

    while current_failed:
        steps += 1
        new_failed = set()

        for n in current_failed:
            if G.nodes[n]["failed"]:
                continue

            G.nodes[n]["failed"] = True
            neighbors = get_intack_neighbours(G, n)
            load = G.nodes[n]["load"]

            if neighbors:
                total_capacity = sum(G.nodes[v]["capacity"] for v in neighbors)

                for neighbor in neighbors:
                    load_share = (G.nodes[neighbor]["capacity"] / total_capacity) * load
                    G.nodes[neighbor]["load"] += load_share
                    if G.nodes[neighbor]["load"] > G.nodes[neighbor]["capacity"]:
                        new_failed.add(neighbor)

            G.nodes[n]["load"] = 0

        failed_per_step.append(len(new_failed))
        current_failed = list(new_failed)

    outputs = calculate_outputs(G)
    return G, steps, failed_per_step, outputs

def get_intack_neighbours(G, node):
    return [
        neighbor
        for neighbor in G.neighbors(node)
        if not G.nodes[neighbor]["failed"]
    ]

def calculate_outputs(G):
    intact_nodes = [n for n in G.nodes() if not G.nodes[n]["failed"]]
    failed_nodes = [n for n in G.nodes() if G.nodes[n]["failed"]]

    intact_subgraph = G.subgraph(intact_nodes)
    largest_cc = max(nx.connected_components(intact_subgraph), key=len, default=set())

    return {
        "num_failed_nodes": len(failed_nodes),
        "num_intact_nodes": len(intact_nodes),
        "size_largest_cc": len(largest_cc)
    }
