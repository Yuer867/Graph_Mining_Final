"""
This is the file of all algorithms used in this project.
Algorithms:
    Greedy: the greedy algorithm without reduction
    DtSingle: the greedy algorithm equipped with the single-vertex reduction proposed by Zheng
    DtTwo: the greedy algorithm equipped with both single-vertex and two-vertex reductions proposed by Zheng
    CutSmall1: the greedy algorithm equipped with the small-cut reduction
    CutSmall2: the greedy algorithm equipped with the small-cut, single-vertex and two-vertex reductions
    Cut: the greedy algorithm equipped with the cut, single-vertex and two-vertex reductions
"""

import networkx as nx
import copy
import time

#####################
# Greedy Algorithms #
#####################
# select the vertex v minimizing d(v)
def GMIN(Graph):
    start_time = time.time()
    G = copy.deepcopy(Graph)
    MIS = list()
    while G.number_of_nodes() != 0:
        remove = list()
        if len(G.edges()) == 0:
            for node in G.nodes():
                MIS.append(node)
                remove.append(node)
            for node in remove:
                G.remove_node(node)
        else:
            weight = dict()
            for node in G.nodes():
                d = nx.degree(G, node)
                if d == 0:
                    MIS.append(node)
                else:
                    weight[node] = d

            target = sorted(weight.items(), key=lambda x: x[1], reverse=False)[0][0]
            MIS.append(target)
            neighbors = nx.all_neighbors(G, target)
            G.remove_node(target)
            for i in neighbors:
                G.remove_node(i)
            for node in MIS:
                if node in G:
                    G.remove_node(node)

    s = 0
    for i in MIS:
        s += Graph.nodes[i]['weight']
    end_time = time.time()
    all_time = round(end_time-start_time, 2)
    return MIS, s, all_time

# select the vertex v maximizing w(v)/d(v)
def GWMIN(Graph):
    start_time = time.time()
    G = copy.deepcopy(Graph)
    MIS = list()
    while G.number_of_nodes() != 0:
        remove = list()
        if len(G.edges()) == 0:
            for node in G.nodes():
                MIS.append(node)
                remove.append(node)
            for node in remove:
                G.remove_node(node)
        else:
            weight = dict()
            for node in G.nodes():
                w = G.nodes[node]['weight']
                d = nx.degree(G, node)
                neighbors = nx.all_neighbors(G, node)
                if d == 0:
                    MIS.append(node)
                else:
                    weight[node] = w / d

            target = sorted(weight.items(), key=lambda x: x[1], reverse=True)[0][0]
            MIS.append(target)
            neighbors = nx.all_neighbors(G, target)
            G.remove_node(target)
            for i in neighbors:
                G.remove_node(i)
            for node in MIS:
                if node in G:
                    G.remove_node(node)
    s = 0
    for i in MIS:
        s += Graph.nodes[i]['weight']
    end_time = time.time()
    all_time = round(end_time - start_time, 2)
    return MIS, s, all_time

# select the vertex v maximizing w(v)/w(N(v))
def GWMIN2(Graph):
    start_time = time.time()
    G = copy.deepcopy(Graph)
    MIS = list()
    while G.number_of_nodes() != 0:
        remove = list()
        if len(G.edges()) == 0:
            for node in G.nodes():
                MIS.append(node)
                remove.append(node)
            for node in remove:
                G.remove_node(node)
        else:
            weight = dict()
            for node in G.nodes():
                w = G.nodes[node]['weight']
                neighbors = nx.all_neighbors(G, node)
                s = 0
                for neighbor in neighbors:
                    s += G.nodes[neighbor]['weight']
                if s == 0:
                    MIS.append(node)
                else:
                    weight[node] = w / s

            target = sorted(weight.items(), key=lambda x: x[1], reverse=True)[0][0]
            MIS.append(target)
            neighbors = nx.all_neighbors(G, target)
            G.remove_node(target)
            for i in neighbors:
                G.remove_node(i)
            for node in MIS:
                if node in G:
                    G.remove_node(node)
    s = 0
    for i in MIS:
        s += Graph.nodes[i]['weight']
    end_time = time.time()
    all_time = round(end_time - start_time, 2)
    return MIS, s, all_time


###############################
# single/two-vertex reduction #
###############################
# single-vertex reduction
def single_vertex_reduction(Graph):
    G = copy.deepcopy(Graph)
    S = []
    while True:
        remove = []
        delta = dict()
        for node in G.nodes():
            if node in remove:
                continue
            delta[node] = 0
            for neighbor in nx.neighbors(G, node):
                delta[node] += G.nodes[neighbor]['weight']
            if G.nodes[node]['weight'] >= delta[node]:
                S.append(node)
                remove.append(node)
                for neighbor in nx.neighbors(G, node):
                    remove.append(neighbor)
        if len(remove) == 0:
            break
        else:
            for node in set(remove):
                G.remove_node(node)
    return G, S

# single/two-vertex reduction
def single_two_vertex_reduction(Graph):
    G = copy.deepcopy(Graph)
    S = []
    # single-vertex reduction
    while True:
        remove = []
        delta = dict()
        for node in G.nodes():
            if node in remove:
                continue
            delta[node] = 0
            for neighbor in nx.neighbors(G, node):
                delta[node] += G.nodes[neighbor]['weight']
            if G.nodes[node]['weight'] >= delta[node]:
                S.append(node)
                remove.append(node)
                for neighbor in nx.neighbors(G, node):
                    remove.append(neighbor)
        if len(remove) == 0:
            break
        else:
            for node in set(remove):
                G.remove_node(node)
    # two-vertex reduction
    while True:
        flag = 0
        status = dict()
        for node in G.nodes():
            status[node] = False
        for u in G.nodes():
            status[u] = True
            T = []
            remove = []
            for v in nx.neighbors(G, u):
                for w in nx.neighbors(G, v):
                    if status[w] == False and (u, w) not in G.edges():
                        T.append(w)
            for v in T:
                neighbors = []
                for neighbor in nx.neighbors(G, u):
                    neighbors.append(neighbor)
                for neighbor in nx.neighbors(G, v):
                    neighbors.append(neighbor)
                neighbors = set(neighbors)
                s = 0
                for neighbor in neighbors:
                    s += G.nodes[neighbor]['weight']
                if G.nodes[u]['weight'] + G.nodes[v]['weight'] >= s:
                    S.append(u)
                    S.append(v)
                    remove = list(neighbors) + [u, v]
                    flag = 1
                    break
            if flag == 0:
                continue
            else:
                for i in remove:
                    G.remove_node(i)
                break
        if flag == 0:
            break
    return G, S

# remove the node with degree one
def remove_single_node(Graph, S):
    remove = []
    for v in Graph.nodes():
        if nx.degree(Graph, v) == 0:
            S.append(v)
            remove.append(v)
    for i in remove:
        Graph.remove_node(i)
    return Graph, S

# determine whether the graph is connected
def is_connect(Graph, nodes):
    for i in nodes:
        for j in nodes:
            if i != j and (i, j) not in Graph.edges():
                return False
    return True

# compute the MWIS of clique
def clique_process(Graph, S):
    components = nx.connected_components(Graph)
    remove = []
    for component in components:
        if is_connect(Graph, list(component)):
            max = 0
            for node in component:
                if Graph.nodes[node]['weight'] > max:
                    max = Graph.nodes[node]['weight']
                    target = node
            S.append(target)
            for node in component:
                remove.append(node)
    for node in remove:
        Graph.remove_node(node)
    return Graph, S

# vertex reduction
def vertex_reduction(Graph):
    G = copy.deepcopy(Graph)
    G, S = single_two_vertex_reduction(G)
    G, S = remove_single_node(G, S)
    G, S = clique_process(G, S)
    return G, S

# DtSingle Algorithm
def DtSingle(Graph):
    G = copy.deepcopy(Graph)
    MIS = []
    while G.number_of_nodes() != 0:
        G, S = single_vertex_reduction(G)
        G, S = remove_single_node(G, S)
        G, S = clique_process(G, S)
        MIS += S
        if G.number_of_nodes() == 0:
            break
        weight = dict()
        for node in G.nodes():
            w = G.nodes[node]['weight']
            d = nx.degree(G, node)
            neighbors = nx.all_neighbors(G, node)
            s = 0
            for neighbor in neighbors:
                s += nx.degree(G, neighbor)
            #    s += G.nodes[neighbor]['weight']
            # weight[node] = w / s
            # weight[node] = w / nx.degree(G, node)
            weight[node] = 1 / nx.degree(G, node)
            # weight[node] = w/(s*d)

        target = sorted(weight.items(), key=lambda x: x[1])[0][0]
        G.remove_node(target)
    s = 0
    for i in MIS:
        s += Graph.nodes[i]['weight']
    return MIS, s

# DtTwo Algorithm
def DtTwo(Graph):
    G = copy.deepcopy(Graph)
    MIS = []
    while G.number_of_nodes() != 0:
        G, S = single_two_vertex_reduction(G)
        G, S = remove_single_node(G, S)
        G, S = clique_process(G, S)
        MIS += S
        if G.number_of_nodes() == 0:
            break
        weight = dict()
        for node in G.nodes():
            w = G.nodes[node]['weight']
            d = nx.degree(G, node)
            neighbors = nx.all_neighbors(G, node)
            s = 0
            for neighbor in neighbors:
                s += nx.degree(G, neighbor)
            #    s += G.nodes[neighbor]['weight']
            #weight[node] = w / s
            #weight[node] = w / nx.degree(G, node)
            weight[node] = 1 / nx.degree(G, node)
            #weight[node] = w/(s*d)

        target = sorted(weight.items(), key=lambda x: x[1])[0][0]
        G.remove_node(target)
    s = 0
    for i in MIS:
        s += Graph.nodes[i]['weight']
    return MIS, s


#######################
# small-cut reduction #
#######################
# small-cut reduction
def small_cut_reduction(Graph, S, cut_dict):
    G = Graph
    remove = []
    small_cut_vertex = []
    for node in G.nodes():
        if nx.degree(G, node) == 1:
            neighbor = list(nx.all_neighbors(G, node))[0]
            small_cut_vertex.append(neighbor)
    small_cut_vertex = list(set(small_cut_vertex))
    for node in small_cut_vertex:
        U = []
        neighbors = list(nx.all_neighbors(G, node))
        for neighbor in neighbors:
            if nx.degree(G, neighbor) == 1:
                U.append(neighbor)
        remove += U
        s = 0
        for u in U:
            s += G.nodes[u]['weight']
        if s > G.nodes[node]['weight']:
            S = S + U
            remove.append(node)
        else:
            for neighbor in U:
                if node in cut_dict:
                    if neighbor in cut_dict:
                        cut_dict[node][0] += ([neighbor] + cut_dict[neighbor][1])
                        cut_dict[node][1] += cut_dict[neighbor][0]
                        _ = cut_dict.pop(neighbor)
                    else:
                        cut_dict[node][0].append(neighbor)
                else:
                    if neighbor in cut_dict:
                        cut_dict[node] = {0: [neighbor] + cut_dict[neighbor][1], 1: cut_dict[neighbor][0]}
                        _ = cut_dict.pop(neighbor)
                    else:
                        cut_dict[node] = {0: [neighbor], 1: []}
                G.nodes[node]['weight'] = G.nodes[node]['weight'] - G.nodes[neighbor]['weight']
    remove = list(set((remove)))
    for node in remove:
        G.remove_node(node)
    return G, S, cut_dict

# CutSmall1 Algorithm
def CutSmall1(Graph):
    G = copy.deepcopy(Graph)
    MIS = []
    cut = dict()
    while G.number_of_nodes() != 0:
        while True:
            S = []
            G, S, cut = small_cut_reduction(G, S, cut)
            G, S = remove_single_node(G, S)
            G, S = clique_process(G, S)
            MIS += S
            if len(S) == 0:
                break
        if G.number_of_nodes() == 0:
            break
        weight = dict()
        for node in G.nodes():
            w = G.nodes[node]['weight']
            d = nx.degree(G, node)
            neighbors = nx.all_neighbors(G, node)
            s = 0
            for neighbor in neighbors:
                #    s += nx.degree(G, neighbor)
                s += G.nodes[neighbor]['weight']
            # weight[node] = w / s
            # weight[node] = w / nx.degree(G, node)
            weight[node] = 1 / nx.degree(G, node)
            # weight[node] = w/(s*d)

        target = sorted(weight.items(), key=lambda x: x[1])[0][0]
        G.remove_node(target)
    for node in cut:
        if node not in MIS:
            MIS = MIS + cut[node][0]
        else:
            MIS = MIS + cut[node][1]
    MIS = list(set(MIS))
    s = 0
    for i in MIS:
        s += Graph.nodes[i]['weight']
    return MIS, s

# CutSmall2 Algorithm
def CutSmall2(Graph):
    G = copy.deepcopy(Graph)
    MIS = []
    cut = dict()
    while G.number_of_nodes() != 0:
        while True:
            G, S = single_two_vertex_reduction(G)
            G, S = remove_single_node(G, S)
            G, S = clique_process(G, S)
            G, cut = cut_reduction(G, cut)
            MIS += S
            if len(S) == 0:
                break
        if G.number_of_nodes() == 0:
            break
        weight = dict()
        for node in G.nodes():
            w = G.nodes[node]['weight']
            d = nx.degree(G, node)
            neighbors = nx.all_neighbors(G, node)
            s = 0
            for neighbor in neighbors:
                #    s += nx.degree(G, neighbor)
                s += G.nodes[neighbor]['weight']
            # weight[node] = w / s
            # weight[node] = w / nx.degree(G, node)
            weight[node] = 1 / nx.degree(G, node)
            # weight[node] = w/(s*d)

        target = sorted(weight.items(), key=lambda x: x[1])[0][0]
        G.remove_node(target)
    for node in cut:
        if node not in MIS:
            MIS = MIS + cut[node][0]
        else:
            MIS = MIS + cut[node][1]
    s = 0
    for i in MIS:
        s += Graph.nodes[i]['weight']
    return MIS, s

# process case 2 of small-cut reduction
def cut_reduction(Graph, cut_dict):
    G = Graph
    remove = []
    for node in G.nodes():
        if nx.degree(G, node) == 1:
            remove.append(node)
            neighbor = list(nx.all_neighbors(G, node))[0]
            if neighbor in cut_dict:
                if node in cut_dict:
                    cut_dict[neighbor][0] += ([node] + cut_dict[node][1])
                    cut_dict[neighbor][1] += cut_dict[node][0]
                    _ = cut_dict.pop(node)
                else:
                    cut_dict[neighbor][0].append(node)
            else:
                if node in cut_dict:
                    cut_dict[neighbor] = {0: [node]+cut_dict[node][1], 1: cut_dict[node][0]}
                    _ = cut_dict.pop(node)
                else:
                    cut_dict[neighbor] = {0: [node], 1: []}
            G.nodes[neighbor]['weight'] = G.nodes[neighbor]['weight'] - G.nodes[node]['weight']
    for node in remove:
        G.remove_node(node)
    return G, cut_dict


#######################
# big-cut reduction #
#######################
# big-cut reduction
def big_cut_reduction(Graph, MIS, big_cut_dict):
    cuts = nx.all_node_cuts(Graph, 1)
    for i in cuts:
        node = list(i)[0]
        break
    G = copy.deepcopy(Graph)
    G.remove_node(node)
    G_list = get_subgraph(G)
    neighbors = nx.all_neighbors(Graph, node)
    for G_sub in G_list:
        G_sub.add_node(node, weight=Graph.nodes[node]['weight'])
    for i in neighbors:
        for G_sub in G_list:
            if i in G_sub.nodes:
                G_sub.add_edge(node, i)
    flag = 0
    new_weight = Graph.nodes[node]['weight']
    for i in range(len(G_list)):
        G_sub = G_list[i]
        G_sub.nodes[node]['weight'] = new_weight
        S1, s1 = Cut(G_sub)
        if node in S1:
            S1.remove(node)
        G_sub.remove_node(node)
        S0, s0 = Cut(G_sub)
        if s0 >= s1:
            MIS += S0
            if node in big_cut_dict:
                MIS += big_cut_dict[node][0]
                _ = big_cut_dict.pop(node)
            if i + 1 < len(G_list):
                flag = 1
            break
        else:
            new_weight = s1 - s0
            for u in S0:
                if node not in big_cut_dict:
                    big_cut_dict[node] = {0: [], 1: []}
                big_cut_dict[node][0] += [u]
                if u in big_cut_dict:
                    if u in S1:
                        continue
                    else:
                        big_cut_dict[node][0] += big_cut_dict[u][1]
                        big_cut_dict[node][1] += big_cut_dict[u][0]
            for w in S1:
                if node not in big_cut_dict:
                    big_cut_dict[node] = {0: [], 1: []}
                big_cut_dict[node][1] += [w]
                if w in big_cut_dict:
                    if w in S0:
                        continue
                    else:
                        big_cut_dict[node][1] += big_cut_dict[w][1]
                        big_cut_dict[node][0] += big_cut_dict[w][0]
            for u in S0:
                if u in big_cut_dict:
                    _ = big_cut_dict.pop(u)
            for w in S1:
                if w in big_cut_dict:
                    _ = big_cut_dict.pop(w)
    if flag == 1:
        for j in range(i+1, len(G_list)):
            G_new = G_list[j]
            G_new.remove_node(node)
            S, _ = Cut(G_new)
            MIS += S
    return 0

# get disconnected components of given graph
def get_subgraph(Graph):
    components = nx.connected_components(Graph)
    G_list = []
    for component in components:
        nodes = list(component)
        edges = []
        for i in component:
            for j in component:
                if (i, j) in Graph.edges:
                    edges.append((i, j))
        G_sub = nx.Graph()
        for node in nodes:
            G_sub.add_node(node, weight = Graph.nodes[node]['weight'])
        G_sub.add_edges_from(edges)
        G_list.append(G_sub)
    G_list.reverse()
    return G_list

# reduction rules containing cut reduction and vertex reduction
def reduction(G, MIS, cut_dict):
    while G.number_of_nodes() != 0:
        while True:
            G, S = vertex_reduction(G)
            G, cut_dict = cut_reduction(G, cut_dict)
            MIS += S
            if G.number_of_nodes() == 0:
                break
            if len(S) == 0:
                if nx.number_connected_components(G) != 1:
                    G_list = get_subgraph(G)
                    for G_sub in G_list:
                        S, _ = Cut(G_sub)
                        MIS += S
                    return 0
                else:
                    if nx.node_connectivity(G) == 1:
                        big_cut_reduction(G, MIS, cut_dict)
                        return 0
                    else:
                        break
        if G.number_of_nodes() == 0:
            break
        weight = dict()
        for node in G.nodes():
            weight[node] = 1 / (nx.degree(G, node) + 1)
        target = sorted(weight.items(), key=lambda x: x[1])[0][0]
        G.remove_node(target)
    return 0

# Cut Algorithm
def Cut(Graph):
    G = copy.deepcopy(Graph)
    MIS = []
    cut_dict = {}
    reduction(G, MIS, cut_dict)
    keys = list(cut_dict.keys())
    keys.reverse()
    for node in keys:
        if node not in MIS:
            MIS = MIS + cut_dict[node][0]
        else:
            MIS = MIS + cut_dict[node][1]
    MIS = list(set(MIS))
    s = 0
    for i in MIS:
        s += Graph.nodes[i]['weight']
    return MIS, s
