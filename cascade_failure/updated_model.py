import pandas as pd
import networkx as nx
import ast


def load_data(edges_path="data/edges.csv", nodes_path="data/nodes.csv"):
    edges = pd.read_csv(edges_path)
    nodes = pd.read_csv(nodes_path)

    nodes["pos"] = nodes["pos"].apply(lambda x: list(ast.literal_eval(x.replace("array", "").replace("(", "").replace(")", ""))))

    G = nx.from_pandas_edgelist(edges, source="source", target="target")

    pos_dict = {row["index"]: row["pos"] for _, row in nodes.iterrows()}
    nx.set_node_attributes(G, pos_dict, "pos")

    print(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    return G

def assign_atributtes(edges_path="data/edges.csv", nodes_path="data/nodes.csv"):
    edges = pd.read_csv(edges_path)
    nodes = pd.read_csv(nodes_path)

    nodes["pos"] = nodes["pos"].apply(lambda x: list(ast.literal_eval(x.replace("array", "").replace("(", "").replace(")", ""))))

    G = nx.from_pandas_edgelist(edges, source="source", target="target")

    pos_dict = {row["index"]: row["pos"] for _, row in nodes.iterrows()}
    nx.set_node_attributes(G, pos_dict, "pos")

    print(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    for n in G.nodes():
        # initial load
        G.nodes[n]["load"] = 1016      # average load (energy consumption) in the western US area
        # uniform capacity
        G.nodes[n]['capacity']=G.nodes[n]["load"]*10
        # all nodes start as operational
        G.nodes[n]["failed"] = False
    return G