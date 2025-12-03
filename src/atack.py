import random
import networkx as nx

def random_node_attack(G0, number_of_nodes=1):
    G = G0.copy()
    failed_nodes = []
    for _ in range(number_of_nodes):
        node = random.choice(list(G))
        G.remove_node(node)
        failed_nodes.append(node)
    
    return failed_nodes

# high degree node attack = high capacity node attack
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

# high betweenness node attack
def high_betweenness_node_attack(G0, number_of_nodes=1):
    G = G0.copy()
    betweenness = nx.betweenness_centrality(G, normalized=True)
    sorted_nodes = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
    
    failed_nodes = []
    for i in range(number_of_nodes):
        node = sorted_nodes[i][0]
        G.remove_node(node)
        failed_nodes.append(node)
    
    return failed_nodes

def high_load_node_attack(G0, number_of_nodes=1):
    G = G0.copy()
    node_loads = {}
    for n in G.nodes():
        node_loads[n] = G.nodes[n]['load']
    
    sorted_nodes = sorted(node_loads.items(), key=lambda x: x[1], reverse=True)
    
    failed_nodes = []
    for i in range(number_of_nodes):
        node = sorted_nodes[i][0]
        G.remove_node(node)
        failed_nodes.append(node)
    
    return failed_nodes

def high_load_capacity_ratio_node_attack(G0, number_of_nodes=1):
    G = G0.copy()
    node_ratios = {}
    for n in G.nodes():
        load = G.nodes[n]['load']
        capacity = G.nodes[n]['capacity']
        ratio = load / capacity
        node_ratios[n] = ratio
    
    sorted_nodes = sorted(node_ratios.items(), key=lambda x: x[1], reverse=True)
    
    failed_nodes = []
    for i in range(number_of_nodes):
        node = sorted_nodes[i][0]
        G.remove_node(node)
        failed_nodes.append(node)
    
    return failed_nodes

def high_load_capacity_ratio_and_degree_node_attack(G0, number_of_nodes=1):
    G = G0.copy()
    node_scores = {}
    for n in G.nodes():
        load = G.nodes[n]['load']
        capacity = G.nodes[n]['capacity']
        degree = G.degree(n)
        ratio = load / capacity
        score = ratio * degree
        node_scores[n] = score
    
    sorted_nodes = sorted(node_scores.items(), key=lambda x: x[1], reverse=True)
    
    failed_nodes = []
    for i in range(number_of_nodes):
        node = sorted_nodes[i][0]
        G.remove_node(node)
        failed_nodes.append(node)
    
    return failed_nodes

#----------------------------------------------------------------
# DC model atack strategies
#----------------------------------------------------------------
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