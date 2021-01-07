# -*- coding: utf-8 -*-

import math
import pandas as pd
import os
import re
import numpy as np
import networkx as nx
import random
import matplotlib.pyplot as plt

import time
import seaborn as sns
from decimal import Decimal
from scipy.stats import kendalltau
import EoN
from queue import Queue
from igraph import Graph as IG
from random import choice
from collections import Counter


def auc(G, y_vector):
    final = {}
    for node in G.nodes():
        x = [0, 1, 2]
        y = y_vector[node]
        auc_value = np.trapz(y, x)
        final[node] = auc_value
    return final

def tree(G, k, cs_dict):
    hight = {}  # 每个节点生成树的高度
    level = {}
    ccs_degree = {}
    for iterator_node in G.nodes():
        q = Queue(maxsize=0)
        q.put((1, iterator_node))  # 第一层是待检验节点，加入到queue中
        #print('node:', iterator_node)
        #print(q.get())
        ccs = [0]  # 累计度数
        ccs.append(cs_dict[iterator_node])
        #print(accu_degree)
        depth = 1
        vis = {}  # key为节点，dict为节点所在的层数
        c = [0]
        while (q.empty() != True):
            vis.clear()
            now_node = q.get()  # 取出当前队列中第一个元素
            vis[now_node[1]] = depth  # 取出元素的层数为depth
            nums = 0
            plus1 = ccs[-1]  # 第一层邻居节点度数累和
            #print(plus1)
            for i in G.adj[now_node[1]]:  # 遍历取出元素的邻居
                #print('node:', i)
                vis[i] = depth + 1   # 取出元素的邻居均加入到vis dict中，value也就是层数均为depth + 1
                q.put((depth + 1, i))  # 取出元素的邻居节点以及其value放入队列中
                nums += 1  # 该层节点个数
                plus1 += cs_dict[i]
                #print(G.degree(i))
            ccs.append(plus1)
            # print("q",q.queue)
            # print("vis",vis)
            # print("c",c)
            nums2 = 0
            plus2 = ccs[-1]
            while (q.empty() != True):
                now_node = q.get()   # 当queue里为待检验节点和树的第二层，第一层邻居挨个取出（2，direct neighbors）
                if (now_node[0] != depth):  #此时depth=1，而queue里除了待检验节点以外，其他都是一层邻居们，标号均为2
                    depth = now_node[0]  # depth = 2
                    if len(c) == 0:
                        c.append(nums + nums2 / 2)
                    else:
                        a = int(nums + nums2 / 2 + c[-1])
                        c.append(a)
                    if depth <= k and plus2 != ccs[-1]: # 控制变量k
                        ccs.append(plus2)
                    nums = 0
                    nums2 = 0
                for node in G.adj[now_node[1]]:  #此时开始遍历第一层邻居的邻居，也就是第二层邻居
                    if node not in vis:
                        #未出现在depth层中node，也就是未加入vis中的节点加入vis中，key为node, value为depth+1
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
        level[iterator_node] = c
        ccs_degree[iterator_node] = ccs
    return hight, level, ccs_degree


def process(filename):

    """
    Network name:
    karate / USpowerGrid / ia-reality / jazz / dolphins / email-univ / ns / USair_unweighted / Political blogs / Router / HI / football / 911 /
    abn / dbn / mbn / Bahia / baydry / Bluthgen / Carpinteria / ca-CSphd/ ca-GrQc/ celegans_metabolic /
    celegans_Phenotypes / crystal / Estero / Everglades / Florida / Galesburg / Galesburg2 / glossGT /
    grass_web / geom / gramdry / Korea1 / Korea2 / Maspalomas / mexican_power / Michigan / Mondego /
    movies / personal / russiantrade / SciMet / sep_fall98 / SmaGri / SmallW / StMarks / stormofswords /
    Sylt / world_trade / yeast_ito / Ythan
    """
    G = nx.read_edgelist("F:/Peggy/node centrality/h-index/data/911.txt", delimiter='\t', nodetype=str)

    global M, N
    N = G.number_of_nodes()
    M = G.number_of_edges()
    print('number of nodes：%d' % (N))
    print('number of edges：%d' % (M))
    density = M / (N * (N - 1) / 2)
    print('density：%f' % density)

    cc = nx.closeness_centrality(G)
    hight, level, y_vector = tree(G, k=2, cs_dict=cc)
    print(y_vector)
    #print(hight)
    #print(level)
    final = auc(G, y_vector)
    print(final)


if __name__ == "__main__":
    filename = "karate.txt"
    process(filename)


