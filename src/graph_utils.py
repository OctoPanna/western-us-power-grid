import networkx as nx
import random

def calculate_edge_lengths(G):
    pos = nx.get_node_attributes(G, "pos")
    for u, v in G.edges():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        length = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        G[u][v]['length'] = length * 1000
    return G

def assign_voltage(length):
    if length > 120: return 345
    elif length > 50: return 230
    else: return 138

def assign_capacity(voltage):
    if voltage == 345: return random.uniform(500, 900)
    if voltage == 230: return random.uniform(200, 400)
    if voltage == 138: return random.uniform(70, 150)
    return random.uniform(40, 100)

def assign_reactance(length_km, voltage):
    X_ohm = 0.0004 * length_km
    X_pu = X_ohm * (100 / (voltage ** 2))
    return X_pu
import random

def assign_node_loads(G, safety_factor=0.5, total_load=50_000):
    degrees = dict(G.degree())
    weights = {n: max(1e-3, deg) for n, deg in degrees.items()}
    Z = sum(weights.values())
    for n, w in weights.items():
        max_load = sum(G[n][v]['capacity_MW'] for v in G.neighbors(n))
        G.nodes[n]["load_MW"] = min((w / Z) * total_load, max_load * safety_factor)

def assign_generators(G, num_generators=20, safety_factor=0.5, max_gen=2000):
    betweenness = dict(nx.betweenness_centrality(G, normalized=True))
    nodes = list(G.nodes())

    weights = [betweenness[n] for n in nodes]

    gen_nodes = random.choices(nodes, weights=weights, k=num_generators) # high degree preference

    for n in G.nodes():
        G.nodes[n]["gen_MW"] = 0.0
    for n in gen_nodes:
        incident_capacity = sum(G[n][v]['capacity_MW'] for v in G.neighbors(n))
        G.nodes[n]["gen_MW"] = min(random.uniform(200, max_gen), incident_capacity * safety_factor)

def total_generation_and_load(G):
    total_gen = sum(G.nodes[n].get('gen_MW', 0.0) for n in G.nodes())
    total_load = sum(G.nodes[n].get('load_MW', 0.0) for n in G.nodes())
    return total_gen, total_load

def scale_generators_to_match_load(G):
    total_gen, total_load = total_generation_and_load(G)
    if total_gen == 0:
        raise ValueError("No generation present to scale.")
    scale = total_load / total_gen
    for n in G.nodes():
        if G.nodes[n].get('gen_MW', 0.0) > 0.0:
            G.nodes[n]['gen_MW'] *= scale
    return G

def assign_grid_attributes(G):
    calculate_edge_lengths(G)
    for u, v, data in G.edges(data=True):
        length = data['length']
        
        # voltage
        V = assign_voltage(length)
        data['voltage_kV'] = V
        
        # capacity
        data['capacity_MW'] = assign_capacity(V) * 20
        
        # reactance
        data['reactance'] = assign_reactance(length, V)

    # node loads
    assign_node_loads(G)

    # generation
    assign_generators(G)

    # scale generation to match load
    scale_generators_to_match_load(G)

    return G
