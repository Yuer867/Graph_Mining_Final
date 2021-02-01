"""
This is the file to compute MWIS by greedy algorithms without reduction.
Three kinds of methods: GMIN, GWMIN, GWMIN2
"""

import algorithms
from data import graph

def compute(file):
    filepath = file + '.txt'
    Graph = graph(filepath)
    print(file)
    _, s, all_time = algorithms.GMIN(Graph)
    print('method 0: ', s)
    print('computation time: ', all_time)
    _, s, all_time = algorithms.GWMIN(Graph)
    print('method 1: ', s)
    print('computation time: ', all_time)
    _, s, all_timee = algorithms.GWMIN2(Graph)
    print('method 2: ', s)
    print('computation time: ', all_time)
    print()

dataset = ['GD98_c', 'USAir', 'email', 'netscience',
           'yeast', 'power', 'geom', 'hep-th',
           'cond-mat', 'vt2010', 'ca-GrQc', 'ca-HepTh']
for i in range(len(dataset)):
    compute(dataset[i])
