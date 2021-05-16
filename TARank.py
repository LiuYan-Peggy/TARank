# -*- coding: utf-8 -*-

“”“
change the parameter in lines 119-122
”“”

import numpy as np
import networkx as nx
import random
from decimal import Decimal
from queue import Queue


def auc(G, y_vector, k):  # calculate the area under curve value
    final = {}
    for node in G.nodes():
        x = [i for i in range(0, k+1)]
        y = y_vector[node]
        auc_value = np.trapz(y, x)
        final[node] = auc_value
    return final


def tree(G, k, cs_dict):
    """
    :param G: original network which is read by networkx
    :param k: user-specified parameter k
    :param cs_dict: node score dict generated by user-specified centality measure
    :return: hight dict including the hight of BFS tree of each node, ccs_degree dict including the final score of each node
    """
    hight = {}  # hight dict of the tree of each node
    ccs_degree = {}  # cumulative score dict
    for iterator_node in G.nodes():
        q = Queue(maxsize=0)
        q.put((1, iterator_node))   # put the tested node into queue, 1 represents teh first level of tree 
        # print('node:', iterator_node)
        # print(q.get())
        ccs = [0]
        ccs.append(cs_dict[iterator_node])
        # print(accu_degree)
        depth = 1
        vis = {}  # key is node, value is the level number
        c = [0]
        while (q.empty() != True):
            vis.clear()
            now_node = q.get()  # get the first node from current queue
            vis[now_node[1]] = depth  # now_node[1] is node name, now_node[0] is the location of now_node[1].
            nums = 0
            plus1 = ccs[-1]
            # print(plus1)
            for i in G.adj[now_node[1]]:  # traverse the neighbors of now_node[1]
                # print('node:', i)
                vis[i] = depth + 1   # add all neighbors into vis dict, the corresponding value is depth+1
                q.put((depth + 1, i))  # put the neighbors into queue in turn
                nums += 1 
                plus1 += cs_dict[i]
                # print(G.degree(i))
            ccs.append(plus1)
            # print("q",q.queue)
            # print("vis",vis)
            # print("c",c)
            nums2 = 0
            plus2 = ccs[-1]
            while (q.empty() != True):
                now_node = q.get()  # if the queue is not empty, continue to get the first node from this queue
                if (now_node[0] != depth):
                    depth = now_node[0]
                    if len(c) == 0:
                        c.append(nums + nums2 / 2)
                    else:
                        a = int(nums + nums2 / 2 + c[-1])
                        c.append(a)
                    if depth <= k and plus2 != ccs[-1]:  # control the parameter k
                        ccs.append(plus2)
                    nums = 0
                    nums2 = 0
                for node in G.adj[now_node[1]]:
                    if node not in vis:

                        vis[node] = depth + 1
                        nums += 1
                        q.put((depth + 1, node))
                        plus2 += cs_dict[node]
                    elif vis[node] > depth:
                        nums += 1
                    elif vis[node] == depth:
                        nums2 += 1
                    else:
                        continue
                # print("q",q.queue)
                # print("vis",vis)
                # print("c",c)
            if nums + nums2 / 2 != 0:
                a = int(nums + nums2 / 2 + c[-1])
                c.append(a)
        hight[iterator_node] = depth
        ccs_degree[iterator_node] = ccs
    return hight, ccs_degree


def process():
    """
    Network name:
    karate / USpowerGrid / ia-reality / jazz / dolphins / email-univ / ns / USair_unweighted / Political blogs / Router / HI / football / 911 /
    abn / dbn / mbn / Bahia / baydry / Bluthgen / Carpinteria / ca-CSphd/ ca-GrQc/ celegans_metabolic /
    celegans_Phenotypes / crystal / Estero / Everglades / Florida / Galesburg / Galesburg2 / glossGT /
    grass_web / geom / gramdry / Korea1 / Korea2 / Maspalomas / mexican_power / Michigan / Mondego /
    movies / personal / russiantrade / SciMet / sep_fall98 / SmaGri / SmallW / StMarks / stormofswords /
    Sylt / world_trade / yeast_ito / Ythan
    """
    G = nx.read_edgelist("karate.txt", delimiter='\t', nodetype=str)

    global M, N
    N = G.number_of_nodes()
    M = G.number_of_edges()
    print('number of nodes：%d' % (N), 'number of edges：%d' % (M))

    # input centrality measure and parameter k
    dc = G.degree()  
    parameter = 2
    
    hight, y_vector = tree(G, k=parameter, cs_dict=dc)
    print(y_vector)
    # print(hight)
    c = 0
    for k, v in y_vector.items():
        if len(v) < parameter + 1:
            print(k, v)
            c += 1
            break
    if c == 0:
        final = auc(G, y_vector, k=parameter)
        print(final)
        compare_ic(G, df, sir_rank_list)
    else:
        print('the hight of a tree/some trees is/are less than %d' % (parameter))


if __name__ == "__main__":
    process()


