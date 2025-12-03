def cascade_failure_equal_load_distribution(G0, failed_nodes0):
    G = G0.copy()
    failed_nodes = failed_nodes0.copy()
    for n in failed_nodes:
        # mark node as failed
        if not G.nodes[n]["failed"]:
            G.nodes[n]["failed"] = True
        
        neighbors = get_intack_neighbours(G, n)
        
        load = G.nodes[n]["load"]

        if neighbors:
            load_per_neighbor = load / len(neighbors) # distribute load equally among neighbors
            for neighbor in neighbors:
                if not G.nodes[neighbor]["failed"]:
                    G.nodes[neighbor]["load"] += load_per_neighbor
                    if G.nodes[neighbor]["load"] > G.nodes[neighbor]["capacity"]:
                        failed_nodes.append(neighbor)
    return G

def cascade_failure_proportional_load_distribution(G0, failed_nodes0):
    G = G0.copy()
    failed_nodes = failed_nodes0.copy()
    for n in failed_nodes:
        # mark node as failed
        if not G.nodes[n]["failed"]:
            G.nodes[n]["failed"] = True
        
        neighbors = get_intack_neighbours(G, n)
        
        load = G.nodes[n]["load"]

        if neighbors:
            total_capacity = sum(G.nodes[neighbor]["capacity"] for neighbor in neighbors if not G.nodes[neighbor]["failed"])
            for neighbor in neighbors:
                if not G.nodes[neighbor]["failed"]:
                    capacity = G.nodes[neighbor]["capacity"]
                    load_share = (capacity / total_capacity) * load
                    G.nodes[neighbor]["load"] += load_share
                    if G.nodes[neighbor]["load"] > G.nodes[neighbor]["capacity"]:
                        failed_nodes.append(neighbor)
    return G

def get_intack_neighbours(G, node):
    neighbors = list(G.neighbors(node))
    for neighbor in neighbors:
        if G.nodes[neighbor]["failed"]:
            neighbors.remove(neighbor)
    return neighbors