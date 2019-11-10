import xml.etree.ElementTree as ET
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def get_matrix_from_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    lines = root.iter('line')
    n = len(root.find('graph').find('points').findall('point')) + 1
    matrix = [[0] * n for i in range(n)]
    for child in lines:
        matrix[int(child.attrib['from'])][int(child.attrib['to'])] = int(child.attrib['weight'])
        matrix[int(child.attrib['to'])][int(child.attrib['from'])] = int(child.attrib['weight'])
    return matrix

def in_path(edge, edges):
    for i in edges:
        if (edge[0] == i[0][0] and edge[1] == i[0][1]) or (edge[1] == i[0][0] and edge[0] == i[0][1]):
            return True
    return False

def show_graph(matrix, edges):
    G = nx.Graph(np.matrix(matrix))
    colors = []
    j = 0
    for i in G.edges():
        if in_path(i, edges):
            colors.append('red')
            j += 1
        else:
            colors.append('black')
    pos=nx.spring_layout(G)
    nx.draw(G, with_labels=True, width = 2, pos=pos, edge_color=colors, edge_cmap=plt.cm.Blues)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.show()

def is_matrix(matrix):
    return len(matrix) > 0 and len(matrix[0]) == len(matrix)

def swap(lst, i, j):
    if i != j:
        lst[i], lst[j] = lst[j], lst[i]

def compare(item1, item2, descending = False):
    if item1 > item2:
        return not descending
    else:
        return descending

def edge_map(edge):
    return edge[1]

def matrix_to_dict(matrix):
    if is_matrix(matrix):
        lst = []
        n = len(matrix)
        for i in range(n):
            for j in range(i, n):
                if matrix[i][j] > 0:
                    lst.append([ [i, j], matrix[i][j] ])
    return lst

def shell_sort(lst, mapping_func, descending = False):
    ln = int(len(lst))
    d = ln
    while True:
        d = int(d / 2)
        if (d <= 0):
            break
        for g in range(d):
            for i in range(d + g, ln, d):
                j = i
                while j >= d and compare(mapping_func(lst[j - d]), mapping_func(lst[j]), descending):
                    swap(lst, j - d, j)
                    j -= d

def get_minimum_spanning_tree_sorted(edges):
    minimum_tree = []
    for edge in edges:
        if verify_on_cicle(edge[0][0], edge[0][1], minimum_tree):
            minimum_tree.append(edge)
    return minimum_tree

def verify_on_cicle(edge1, edge2, graph):
    return compare_nodes(get_nodes(edge1, graph), get_nodes(edge2, graph))

def get_nodes(node, graph):
    nodes = []
    for edge in graph:
        if node == edge[0][0]:
            g = graph.copy()
            g.remove(edge)
            nodes.extend(get_nodes(edge[0][1], g))
            nodes.append(edge[0][1])
        elif node == edge[0][1]:
            g = graph.copy()
            g.remove(edge)
            nodes.extend(get_nodes(edge[0][0], g))
            nodes.append(edge[0][0])
    return nodes

def compare_nodes(nodes1, nodes2):
    for i in nodes1:
        for j in nodes2:
            if i == j:
                return False
    return True

def get_minimum_spanning_tree(matrix):
    lst = matrix_to_dict(matrix)
    shell_sort(lst, edge_map)
    return get_minimum_spanning_tree_sorted(lst)


def main():
    matrix = get_matrix_from_file('graph_data.xml')

    lst = get_minimum_spanning_tree(matrix)
    show_graph(matrix, lst)


main()