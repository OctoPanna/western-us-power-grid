import networkx as nx
import random

def assign_atributes(G):    
    for n in G.nodes():
        # capacity based on degree
        G.nodes[n]["capacity"] = G.degree[n] * random.uniform(10, 50)
        # initial load between 10% and 80% of capacity
        G.nodes[n]["load"] = G.nodes[n]["capacity"] * random.uniform(0.1, 0.75)
        # all nodes start as operational
        G.nodes[n]["failed"] = False

