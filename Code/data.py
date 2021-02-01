"""
This is the file of function to process data.
"""

import networkx as nx
import numpy as np
import re

# Convert txt file to a networkx graph.
# Input:
#       file: name of txt file
#       seed: random seed
# Output:
#       Graph: a networkx graph
def graph(file, seed = 0):
    filepath = 'Data/' + file
    f = open(filepath, 'rt')
    lines = f.readlines()
    f.close()
    nodes = []
    edges = []
    for line in lines:
        item = re.findall('\(.+,.+\)', line)[0]
        x, y = item[1:-1].split(',')
        if x == y:
            continue
        edges.append((int(x), int(y)))
        nodes.append(int(x))
        nodes.append(int(y))
    node_num = max(list(set(nodes)))
    nodes = [i for i in range(1, node_num+1)]
    random = np.random.RandomState(seed)
    weight = random.randint(1, 100, size= node_num)
    Graph = nx.Graph()
    for node in nodes:
        Graph.add_node(node, weight=weight[node - 1])
    Graph.add_edges_from(edges)
    return Graph
