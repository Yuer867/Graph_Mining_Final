"""
This is the file to compute statistics of graphs.
Statistics: number of vertices and edges
"""

from data import graph

def compute(file):
    filepath = file + '.txt'
    Graph = graph(filepath)
    print(file)
    print('number of vertices:', Graph.number_of_nodes())
    print('number of edges:', Graph.number_of_edges())
    print()

dataset = ['GD98_c', 'USAir', 'email', 'netscience',
           'yeast', 'power', 'geom', 'hep-th',
           'cond-mat', 'vt2010', 'ca-GrQc', 'ca-HepTh']
for i in range(len(dataset)):
    compute(dataset[i])