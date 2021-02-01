"""
This is the file to compute MWIS by greedy algorithm with small-cut reduction.
Set 'vertex = False' to compute MWIS only with small-cut reduction;
Set 'vertex = True' to compute MWIS with both small-cut and single/two-vertex reduction;
"""

import algorithms
from data import graph
import time

def compute(file, vertex = True):
    filepath = file + '.txt'
    Graph = graph(filepath)
    print(file)
    start_time = time.time()
    if vertex == True:
        S, s = algorithms.CutSmall2(Graph)  # small_cut + vertex reduction
    else:
        S, s = algorithms.CutSmall1(Graph)  # small_cut reduction
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
    print('small-cut reduction')
    compute(dataset[i], vertex=False)
    print('small-cut + veretx reduction')
    compute(dataset[i], vertex=True)
