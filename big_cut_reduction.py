"""
This is the file to compute MWIS by greedy algorithm with cut and vertex reduction.
"""

import algorithms
from data import graph
import time

def compute(file):
    filepath = file + '.txt'
    Graph = graph(filepath)
    print(file)
    start_time = time.time()
    S, s = algorithms.Cut(Graph)  # cut + vertex reduction
    S = list(set(S))
    for i in S:
        for j in S:
            if i != j and (i, j) in Graph.edges:
                print('Wrong')
    end_time = time.time()
    print('weights:', s)
    print(round(end_time - start_time, 2))

dataset = ['GD98_c', 'USAir', 'email', 'netscience',
           'yeast', 'power', 'geom', 'hep-th',
           'cond-mat', 'vt2010', 'ca-GrQc', 'ca-HepTh']
for i in range(len(dataset)):
    compute(dataset[i])




