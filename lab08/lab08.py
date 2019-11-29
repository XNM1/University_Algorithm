import xml.etree.ElementTree as ET
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from math import inf

def get_matrix_from_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    lines = root.iter('line')
    n = len(root.find('graph').find('points').findall('point')) + 1
    matrix = [[0] * n for i in range(n)]
    for child in lines:
        matrix[int(child.attrib['from'])][int(child.attrib['to'])] = int(child.attrib['power'])
        matrix[int(child.attrib['to'])][int(child.attrib['from'])] = int(child.attrib['power'])
    return matrix

def in_path(edge, path):
    for i in range(len(path)):
        if (edge[0] == path[i - 1] and edge[1] == path[i]) or (edge[1] == path[i - 1] and edge[0] == path[i]):
            return True
    return False

def show_graph(matrix, flow, start, end):
    G = nx.Graph(np.matrix(matrix))
    colors = []
    j = 0
    for i in G.edges():
        if flow[i[0]][i[1]] > 0:
            colors.append('red')
            j += 1
        else:
            colors.append('black')
    pos=nx.spring_layout(G)
    nx.draw(G, with_labels=True, width = 2, pos=pos, edge_color=colors, edge_cmap=plt.cm.Blues)
    labels = { e: str(flow[e[0]][e[1]]) + "/" + str(matrix[e[0]][e[1]]) for e in G.edges() }
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    nx.draw_networkx_nodes(G,pos, nodelist=[start], node_color='r')
    nx.draw_networkx_nodes(G,pos, nodelist=[end], node_color='g')
    plt.show()

def get_children(matrix, node):
    return [i for i, k in enumerate(matrix[node]) if k != 0]

def dfs(matrix, start, end, path, pathes):
    path.append(start)
    if start != end:
        for child in get_children(matrix, start):
            if child not in path:
                dfs(matrix, child, end, path, pathes)
                path.remove(child)
    else:
        pathes.append(path.copy())

def find_augment_path(matrix, flow, start, end, pathes):
    for path in pathes:
        is_augment = True
        for i in range(1, len(path)):
            if not (matrix[path[i - 1]][path[i]] - flow[path[i - 1]][path[i]] > 0):
                is_augment = False
                break
        if is_augment:
            return path
    return None

def get_bottleneck(matrix, flow, path):
    min_flow = inf
    for i in range(1, len(path)):
        if matrix[path[i - 1]][path[i]] - flow[path[i - 1]][path[i]] < min_flow:
            min_flow = matrix[path[i - 1]][path[i]] - flow[path[i - 1]][path[i]]
    return min_flow

def set_flow(matrix, flow, path, min_flow):
    for i in range(1, len(path)):
        if flow[path[i - 1]][path[i]] + min_flow > matrix[path[i - 1]][path[i]]:
            flow[path[i - 1]][path[i]] -= min_flow
            flow[path[i]][path[i - 1]] -= min_flow
        else:
            flow[path[i - 1]][path[i]] += min_flow
            flow[path[i]][path[i - 1]] += min_flow

def max_flow(matrix, start, end):
    #init
    pathes = []
    dfs(matrix, start, end, [], pathes)
    pathes.reverse()
    path = []
    n = len(matrix)
    flow = [[0] * n for i in range(n)]
    while True:
        path = find_augment_path(matrix, flow, start, end, pathes)
        if path is None:
            return flow
        bottleneck = get_bottleneck(matrix, flow, path)
        set_flow(matrix, flow, path, bottleneck)

def is_matrix(matrix):
    return len(matrix) > 0 and len(matrix[0]) == len(matrix)

def main():
    matrix = get_matrix_from_file('graph_data.xml')
    start = 1
    end = 11
    flow = max_flow(matrix, start, end)
    sum = 0
    for child in get_children(flow, start):
        sum += flow[child][start]
    print("Max flow: " + str(sum))
    show_graph(matrix, flow, start, end)


main()