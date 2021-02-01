"""
This is the file to compute MWIS by greedy algorithms equipped with vertex reductions.
Set 'single = True' to compute MWIS only with single-vertex reduction;
Set 'single = False' to compute MWIS with both single and two-vertex reduction.
"""

import algorithms
from data import graph
import time

def compute(file, single = True):
    filepath = file + '.txt'
    Graph = graph(filepath)
    print(file)
    start_time = time.time()
    if single == True:
        S, s = PJ2.MIS_reduction4(Graph)  # single vertex reduction
    else:
        S, s = algorithms.DtTwo(Graph)  # single/two vertex reduction
    end_time = time.time()
    print('weights:', s)
    print(round(end_time - start_time, 2))

dataset = ['GD98_c', 'USAir', 'email', 'netscience',
           'yeast', 'power', 'geom', 'hep-th',
           'cond-mat', 'vt2010', 'ca-GrQc', 'ca-HepTh']
for i in range(len(dataset)):
    print('single-vertex reduction')
    compute(dataset[i], single=True)
    print('single/two-vertex reduction')
    compute(dataset[i], single=False)
