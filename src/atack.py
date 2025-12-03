import random

def random_node_attack(G0, number_of_nodes=1):
    G = G0.copy()
    failed_nodes = []
    for _ in range(number_of_nodes):
        node = random.choice(list(G))
        G.remove_node(node)
        failed_nodes.append(node)
    
    return failed_nodes

def high_capacity_node_attack(G0, number_of_nodes=1):
    G = G0.copy()
    node_capacities = {}
    for n in G.nodes():
        incident_capacity = sum(G[n][v]['capacity_MW'] for v in G.neighbors(n))
        node_capacities[n] = incident_capacity
    
    sorted_nodes = sorted(node_capacities.items(), key=lambda x: x[1], reverse=True)
    
    failed_nodes = []
    for i in range(number_of_nodes):
        node = sorted_nodes[i][0]
        G.remove_node(node)
        failed_nodes.append(node)
    
    return failed_nodes

def random_generator_node_attack(G0, number_of_nodes=1):
    G = G0.copy()
    gen_nodes = [n for n in G.nodes() if G.nodes[n].get('gen_MW', 0.0) > 0.0]
    
    if len(gen_nodes) == 0:
        raise ValueError("No generator nodes found in the graph.")
    
    failed_nodes = []
    for _ in range(number_of_nodes):
        if len(gen_nodes) == 0:
            print("No more generator nodes to attack.")
            break
        node = random.choice(gen_nodes)
        G.remove_node(node)
        failed_nodes.append(node)
        gen_nodes.remove(node) 
    
    return failed_nodes

def random_load_node_attack(G0, number_of_nodes=1):
    G = G0.copy()
    load_nodes = [n for n in G.nodes() if G.nodes[n].get('load_MW', 0.0) > 0.0]
    
    if len(load_nodes) == 0:
        raise ValueError("No load nodes found in the graph.")
    
    failed_nodes = []
    for _ in range(number_of_nodes):
        if len(load_nodes) == 0:
            print("No more load nodes to attack.")
            break
        node = random.choice(load_nodes)
        G.remove_node(node)
        failed_nodes.append(node)
        load_nodes.remove(node) 
    
    return failed_nodes

def high_capacity_high_voltage_node_attack(G0, number_of_nodes=1):
    G = G0.copy()
    node_scores = {}
    for n in G.nodes():
        incident_capacity = sum(G[n][v]['capacity_MW'] for v in G.neighbors(n))
        voltage_sum = sum(G[n][v]['voltage_kV'] for v in G.neighbors(n))
        score = incident_capacity * voltage_sum
        node_scores[n] = score
    
    sorted_nodes = sorted(node_scores.items(), key=lambda x: x[1], reverse=True)
    
    failed_nodes = []
    for i in range(number_of_nodes):
        node = sorted_nodes[i][0]
        G.remove_node(node)
        failed_nodes.append(node)
    
    return failed_nodes

def high_degree_node_attack(G0, number_of_nodes=1):
    G = G0.copy()
    node_degrees = dict(G.degree())
    sorted_nodes = sorted(node_degrees.items(), key=lambda x: x[1], reverse=True)
    
    failed_nodes = []
    for i in range(number_of_nodes):
        node = sorted_nodes[i][0]
        G.remove_node(node)
        failed_nodes.append(node)
    
    return failed_nodes