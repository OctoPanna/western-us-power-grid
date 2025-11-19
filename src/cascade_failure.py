import time
import random
import numpy as np

def cascade_failure(graph, initial_failed_edges, threshold=0.5, max_seconds=300):
    start_time = time.time()
    G = graph.copy()
    failed_edges = list(initial_failed_edges)
    all_failed_edges = set(tuple(sorted(e)) for e in failed_edges)

    # remove initial failed edges
    for e in failed_edges:
        if G.has_edge(*e):
            G.remove_edge(*e)

    while failed_edges and (time.time() - start_time) < max_seconds:
        new_failures = []
        for u, v in failed_edges:
            for node in (u, v):
                for neighbor in list(G.neighbors(node)):
                    candidate_edge = tuple(sorted((node, neighbor)))
                    if candidate_edge not in all_failed_edges and G.has_edge(*candidate_edge):
                        if random.random() < threshold:
                            new_failures.append(candidate_edge)
                            all_failed_edges.add(candidate_edge)
                            G.remove_edge(*candidate_edge)
        failed_edges = new_failures

    return G, all_failed_edges

def create_matrix_B(G):
    nodes = list(G.nodes())
    n = len(nodes)

    B = np.zeros((n, n))

    node_index = {n: i for i, n in enumerate(nodes)}

    for u, v, data in G.edges(data=True):
        i = node_index[u]
        j = node_index[v]
        x = data['reactance']
        b = 1 / x
        B[i, j] -= b
        B[j, i] -= b
        B[i, i] += b
        B[j, j] += b

    return B

def solve_dc_flow(G, S_base=100.0, slack_node=None):
    """
    G: graph with
        node attributes: gen_MW, load_MW
        edge attribute: reactance (X)
    S_base: base power in MVA
    slack_node: node to use as slack (if None, use first node)

    returns: edge_flows_MW dict keyed by (u,v) with flow from u->v in MW
    """
    nodes = list(G.nodes())
    B = create_matrix_B(G)
    node_index = {n: i for i, n in enumerate(nodes)}

    # net injections
    P = np.zeros(len(nodes), dtype=float)
    for n in nodes:
        idx = node_index[n]
        gen = G.nodes[n].get('gen_MW', 0.0)
        load = G.nodes[n].get('load_MW', 0.0)
        P[idx] = (gen - load) / S_base

    # slack node
    if slack_node is None:
        slack_idx = 0
    else:     
        slack_idx = node_index[slack_node]

    # remove slack row/col to create B_reduced (invertible)
    mask = [i for i in range(len(nodes)) if i != slack_idx]
    B_reduced = B[np.ix_(mask, mask)]
    P_reduced = P[mask]

    # solve for reduced angles
    try:
        theta_reduced = np.linalg.pinv(B_reduced) @ P_reduced
    except np.linalg.LinAlgError:
        raise ValueError("ERROR :(")
    
    # recreate theta
    theta = np.zeros(len(nodes), dtype=float)
    for i_reduced, i_original in enumerate(mask):
        theta[i_original] = theta_reduced[i_reduced]

    # theta for slack node is zero
    theta[slack_idx] = 0.0

    # compute flows on edges convert to MW
    edge_flows_MW = {}
    for u, v, data in G.edges(data=True):
        i = node_index[u]
        j = node_index[v]
        X = data.get('reactance')
        if X is None or X == 0:
            f_MW = 0.0
        else:
            f_pu = (theta[i] - theta[j]) / X
            f_MW = f_pu * S_base
            
        edge_flows_MW[(u, v)] = f_MW

    return edge_flows_MW

def cascade_simulation(G0, S_base=100.0, trip_threshold=1.0, max_iter=100, slack_node=None):
    """
    G0: original graph
    trip_threshold: trip if |flow_MW| > capacity_MW * trip_threshold -> for tolerance
    max_iter: maximum number of cascade iterations
    slack_node: node to use as slack (if None, use first node)

    returns: a history list of states and final graph
    """
    G = G0.copy()
    history = []
    total_load_initial = sum(G.nodes[n].get('load_MW', 0.0) for n in G.nodes())

    for i in range(max_iter):
        edge_flows_MW = solve_dc_flow(G, S_base=S_base, slack_node=slack_node)
        
        # compute overloaded edges
        overloaded = []
        for (u, v), flow in edge_flows_MW.items():
            capacity = G.edges[u, v].get('capacity_MW', np.inf)
            if abs(flow) > capacity * trip_threshold:
                overloaded.append((u, v, flow, capacity))

        history.append({
            'iteration': i,
            'num_edges': G.number_of_edges(),
            'num_nodes': G.number_of_nodes(),
            'overloaded_count': len(overloaded),
            'overloaded_edges': [(u, v) for (u, v, _, _) in overloaded],
            'edge_flows_MW': edge_flows_MW.copy()
        })

        if len(overloaded) == 0:
            break # no more overloads, stop

        # remove overloaded edges (simulate trip)
        for u, v, _, _ in overloaded:
            if G.has_edge(u, v):
                G.remove_edge(u, v)

    total_load_remaining = sum(G.nodes[n].get('load_MW', 0.0) for n in G.nodes())
    load_served_fraction = total_load_remaining / total_load_initial if total_load_initial > 0 else 1.0
    result = {
        'history': history,
        'graph': G,
        'initial_total_load_MW': total_load_initial,
        'final_total_load_MW': total_load_remaining,
        'load_served_fraction': load_served_fraction
    }
    return result