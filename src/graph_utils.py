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
    if voltage == 345: return 1000
    if voltage == 230: return 500
    if voltage == 138: return 200
    return 100

def assign_reactance(length_km, voltage):
    if voltage == 345: X_ohm = 0.30 * length_km
    if voltage == 230: X_ohm = 0.45 * length_km
    if voltage == 138: X_ohm = 0.60 * length_km
    S_base = 100
    X_pu = X_ohm * (S_base / (voltage * 1e3)**2)
    return X_pu

def assign_node_loads(G, safety_factor=0.3):
    for n in G.nodes():
        incident_capacity = sum(G[n][v]['capacity_MW'] for v in G.neighbors(n))
        G.nodes[n]['load_MW'] = incident_capacity * safety_factor

def assign_generators(G, num_generators=400, max_gen=500):
    betweenness = nx.betweenness_centrality(G, normalized=True)
    nodes = list(G.nodes())
    weights = [betweenness[n] for n in nodes]
    gen_nodes = random.choices(nodes, weights=weights, k=num_generators)

    for n in G.nodes():
        G.nodes[n]["gen_MW"] = 0.0

    for n in gen_nodes:
        incident_capacity = sum(G[n][v]['capacity_MW'] for v in G.neighbors(n))
        G.nodes[n]["gen_MW"] = min(random.uniform(50, max_gen), incident_capacity * 0.7)

def total_generation_and_load(G):
    total_gen = sum(G.nodes[n].get('gen_MW', 0.0) for n in G.nodes())
    total_load = sum(G.nodes[n].get('load_MW', 0.0) for n in G.nodes())
    return total_gen, total_load

def scale_generators_to_match_load(G):
    total_gen, total_load = total_generation_and_load(G)
    if total_gen == 0:
        return G
    scale = total_load / total_gen
    for n in G.nodes():
        if G.nodes[n].get('gen_MW', 0.0) > 0.0:
            incident_capacity = sum(G[n][v]['capacity_MW'] for v in G.neighbors(n))
            G.nodes[n]['gen_MW'] = min(G.nodes[n]['gen_MW'] * scale, incident_capacity * 0.7)
    return G

def assign_DC_attributes(G):
    calculate_edge_lengths(G)

    for u, v, data in G.edges(data=True):
        length = data['length']
        
        # Voltage
        V = assign_voltage(length)
        data['voltage_kV'] = V
        
        # Capacity
        data['capacity_MW'] = assign_capacity(V)
        
        # Reactance
        data['reactance'] = assign_reactance(length, V)

    # Assign small loads proportional to incident capacities
    assign_node_loads(G, safety_factor=0.05)

    # Assign many distributed generators
    assign_generators(G, num_generators=round(0.05 * G.number_of_nodes()), max_gen=300)

    # Scale generators to match total load while respecting local limits
    scale_generators_to_match_load(G)

    return G

def assign_atributes(G):    
    for n in G.nodes():
        G.nodes[n]["capacity"] = G.degree[n] * random.randint(1, 10)
        G.nodes[n]["load"] = G.nodes[n]["capacity"] * random.uniform(0.1, 0.8)
        G.nodes[n]["failed"] = False