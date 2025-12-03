import random
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

def load_data_with_attributes(edges_path="data/edges.csv", nodes_path="data/nodes_lc.csv"):
    edges = pd.read_csv(edges_path)
    nodes = pd.read_csv(nodes_path)

    G = nx.from_pandas_edgelist(
        edges,
        source="source",
        target="target",
        create_using=nx.Graph(),
    )

    for _, row in nodes.iterrows():
        n = row["index"]

        node_attrs = {}

        if {"pos_x", "pos_y"}.issubset(nodes.columns):
            node_attrs["pos"] = [row["pos_x"], row["pos_y"]]

        for col in nodes.columns:
            if col not in ["index", "pos_x", "pos_y"]:
                node_attrs[col] = row[col]

        G.add_node(n, **node_attrs)

    print(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    return G

def save_nodes(G, nodes_path="data/nodes_lc.csv"):
    nodes_data = []
    for n, data in G.nodes(data=True):
        node_info = {"index": n}
        if "pos" in data and isinstance(data["pos"], (list, tuple)) and len(data["pos"]) == 2:
            node_info["pos_x"] = data["pos"][0]
            node_info["pos_y"] = data["pos"][1]
            data = {k: v for k, v in data.items() if k != "pos"}
        node_info.update(data)
        nodes_data.append(node_info)
    nodes_df = pd.DataFrame(nodes_data)
    nodes_df.to_csv(nodes_path, index=False)

    print(f"Graph saved: {G.number_of_nodes()} nodes")

def save_data_DC(G, edges_path="data/edges_with_attributes.csv", nodes_path="data/nodes_with_attributes.csv"):
    edges_data = []
    for u, v, data in G.edges(data=True):
        edge_info = {"source": u, "target": v}
        edge_info.update(data)
        edges_data.append(edge_info)
    edges_df = pd.DataFrame(edges_data)
    edges_df.to_csv(edges_path, index=False)

    nodes_data = []
    for n, data in G.nodes(data=True):
        node_info = {"index": n}
        if "pos" in data and isinstance(data["pos"], (list, tuple)) and len(data["pos"]) == 2:
            node_info["pos_x"] = data["pos"][0]
            node_info["pos_y"] = data["pos"][1]
            data = {k: v for k, v in data.items() if k != "pos"}
        node_info.update(data)
        nodes_data.append(node_info)
    nodes_df = pd.DataFrame(nodes_data)
    nodes_df.to_csv(nodes_path, index=False)

    print(f"Graph saved: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")


def load_data_with_atributes_DC(edges_path="data/edges_with_attributes.csv", nodes_path="data/nodes_with_attributes.csv"):
    edges = pd.read_csv(edges_path)
    nodes = pd.read_csv(nodes_path)

    edge_attr_cols = [col for col in edges.columns if col not in ["source", "target"]]

    G = nx.from_pandas_edgelist(
        edges,
        source="source",
        target="target",
        edge_attr=edge_attr_cols,
        create_using=nx.Graph(),
    )

    for _, row in nodes.iterrows():
        n = row["index"]

        node_attrs = {}

        if {"pos_x", "pos_y"}.issubset(nodes.columns):
            node_attrs["pos"] = [row["pos_x"], row["pos_y"]]

        for col in nodes.columns:
            if col not in ["index", "pos_x", "pos_y"]:
                node_attrs[col] = row[col]

        G.add_node(n, **node_attrs)

    print(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    return G