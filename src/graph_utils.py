import networkx as nx
import random

def assign_atributes_based_on_degree(G):    
    for n in G.nodes():
        G.nodes[n]["capacity"] = G.degree[n] * random.uniform(10, 50)
        G.nodes[n]["load"] = G.nodes[n]["capacity"] * random.uniform(0.1, 0.75)
        G.nodes[n]["failed"] = False

def assign_atributes_based_on_edge_length(G):    
    for n in G.nodes():
        G.nodes[n]["capacity"] = G.degree[n] * random.uniform(10, 50)
        G.nodes[n]["load"] = G.nodes[n]["capacity"] * random.uniform(0.1, 0.75)
        G.nodes[n]["failed"] = False

