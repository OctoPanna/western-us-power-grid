import random
import pandas as pd
import networkx as nx
import ast

def load_data():
    edges = pd.read_csv("data/edges.csv")
    nodes = pd.read_csv("data/nodes.csv")

    nodes["pos"] = nodes["pos"].apply(lambda x: list(ast.literal_eval(x.replace("array", "").replace("(", "").replace(")", ""))))

    G = nx.from_pandas_edgelist(edges, source="source", target="target")

    pos_dict = {row["index"]: row["pos"] for _, row in nodes.iterrows()}
    nx.set_node_attributes(G, pos_dict, "pos")

    print(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    return G