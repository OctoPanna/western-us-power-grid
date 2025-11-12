import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from networkx.algorithms.community import girvan_newman

node_coord=pd.read_csv('nodes.csv')
edges=pd.read_csv('edges.csv')
edges = list(zip(edges['source'], edges['target']))

G = nx.Graph()
G.add_edges_from(edges)

comp = girvan_newman(G)
communities = next(comp)

partition = {node: i for i, comm in enumerate(communities) for node in comm}

pos = {row['id']: (row['x'], row['y']) for _, row in node_coord.iterrows()}

colors = [partition[node] for node in G.nodes()]

plt.figure(figsize=(7,6))
nx.draw(G, pos, node_color=colors, with_labels=True, cmap=plt.cm.tab10, node_size=300)
plt.title("Network Clusters")
plt.show()
print('Is this working?')