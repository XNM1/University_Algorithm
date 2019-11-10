from math import inf
from collections import deque
import PriorityQueue as pq
import sys
import xml.etree.ElementTree as ET
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def is_matrix(matrix):
    return len(matrix) > 0 and len(matrix[0]) == len(matrix)

def get_children(matrix, node):
    return [i for i, k in enumerate(matrix[node]) if k != 0]

def heuristic(node, end, matrix):
    return min(matrix[node]) - max(matrix[node])

def heuristic2(node, end, matrix):
    return -100 if node == end else min(matrix[node]) - max(matrix[node])

def get_min_without_done(marks, done_marks):
    min_ = inf
    mini = 0
    for i, v in enumerate(marks):
        if i not in done_marks and v < min_:
            min_ = v
            mini = i
    return mini

def del_repeats(mylist):
    newlist = []
    for i in mylist:
        if i not in newlist:
            newlist.append(i)
    return newlist

def compare_one(dej_cl, dej_cmp):
    if dej_cl is not None and dej_cmp is not None and len(dej_cmp[1]) > 0:
        nodes1 = dej_cl[0]
        nodes2 = dej_cmp[0]
        len_iterations = (len(nodes1)/len(nodes2) - 1) * 100
        path1 = dej_cl[1]
        path2 = dej_cmp[1]
        j = 0
        for i in range(len(path1)):
            if len(path2) > 0 and path1[i] == path2[i]:
                j += 1
            else:
                break
        if j != 0:
            errors = (len(path1)/j - 1) * 100
            return [len_iterations, errors]
        else:
            return [len_iterations, len(path1)]
    else:
        return [0.0, 0.0]

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

def in_path(edge, path):
    for i in range(len(path)):
        if (edge[0] == path[i - 1] and edge[1] == path[i]) or (edge[1] == path[i - 1] and edge[0] == path[i]):
            return True
    return False

def show_graph(matrix, path):
    G = nx.Graph(np.matrix(matrix))
    colors = []
    j = 0
    for i in G.edges():
        if in_path(i, path):
            colors.append('red')
            j += 1
        else:
            colors.append('black')
    pos=nx.spring_layout(G)
    nx.draw(G, with_labels=True, width = 2, pos=pos, edge_color=colors, edge_cmap=plt.cm.Blues)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.show()

def bfs_classic(matrix, start):
    if is_matrix(matrix):
        #init
        n = len(matrix)
        visited = [False] * n
        queue = deque()
        path = [] #*not importend
        #init node
        visited[start] = True
        queue.append(start)
        while queue:
            node = queue.popleft()
            path.append(node) #*not importend
            for child in get_children(matrix, node):
                if not visited[child]:
                    queue.append(child)
                    visited[child] = True
        return path

def dijkstra_classic(matrix, start):
    if is_matrix(matrix):
        #init
        n = len(matrix)
        visited = [False] * n
        done_marks = [False] * n
        queue = deque()
        marks = [inf] * n
        path = [[]] * n #*not importend
        #init node
        visited[start] = True
        marks[start] = 0
        queue.append(start)
        path[start].append(start) #*not importend
        while queue:
            node = queue.popleft()
            for child in get_children(matrix, node):
                if not done_marks[child] and (marks[node] + matrix[node][child]) < marks[child]:
                        marks[child] = marks[node] + matrix[node][child]
                        path[child] = [] #*not importend
                        path[child].extend(path[node]) #*not importend
                        path[child].append(child) #*not importend
                if not visited[child]:
                    queue.append(child)
                    visited[child] = True
            done_marks[node] = True
        return path

def dijkstra_classic_search(matrix, start, end):
    if is_matrix(matrix):
        #init
        n = len(matrix)
        visited = [False] * n
        done_marks = [False] * n
        queue = deque()
        marks = [inf] * n
        path = [[]] * n #*not importend
        nodes = []
        #init node
        visited[start] = True
        marks[start] = 0
        queue.append(start)
        path[start].append(start) #*not importend
        while queue:
            node = queue.popleft()
            nodes.append(node)
            if node == end:
                return [nodes, path[node]]
            for child in get_children(matrix, node):
                if not done_marks[child] and (marks[node] + matrix[node][child]) < marks[child]:
                        marks[child] = marks[node] + matrix[node][child]
                        path[child] = [] #*not importend
                        path[child].extend(path[node]) #*not importend
                        path[child].append(child) #*not importend
                if not visited[child]:
                    queue.append(child)
                    visited[child] = True
            done_marks[node] = True

def dijkstra_priority_search(matrix, start, end):
    if is_matrix(matrix):
        #init
        n = len(matrix)
        visited = [False] * n
        done_marks = [False] * n
        queue = pq.PriorityQueue()
        marks = [inf] * n
        path = [[]] * n #*not importend
        nodes = []
        #init node
        visited[start] = True
        marks[start] = 0
        queue.push(start, 0)
        path[start].append(start) #*not importend
        while queue.len() > 0:
            node = queue.get()
            nodes.append(node)
            if node == end:
                return [nodes, path[node]]
            for child in get_children(matrix, node):
                if not done_marks[child] and (marks[node] + matrix[node][child]) < marks[child]:
                        marks[child] = marks[node] + matrix[node][child]
                        queue.push(child, -marks[child])
                        path[child] = [] #*not importend
                        path[child].extend(path[node]) #*not importend
                        path[child].append(child) #*not importend
                if not visited[child]:
                    visited[child] = True
            done_marks[node] = True

def a_star(matrix, start, end, heuristic):
    if is_matrix(matrix):
        #init
        n = len(matrix)
        visited = [False] * n
        done_marks = [False] * n
        queue = pq.PriorityQueue()
        marks = [inf] * n
        path = [[]] * n #*not importend\
        nodes = []
        #init node
        visited[start] = True
        marks[start] = 0
        queue.push(start, 0)
        path[start].append(start) #*not importend
        while queue.len() > 0:
            node = queue.get()
            nodes.append(node)
            if node == end:
                return [nodes, path[node]]
            for child in get_children(matrix, node):
                if not done_marks[child] and (marks[node] + matrix[node][child]) < marks[child]:
                        marks[child] = marks[node] + matrix[node][child]
                        queue.push(child, -(marks[child] + heuristic(child, end, matrix)))
                        path[child] = [] #*not importend
                        path[child].extend(path[node]) #*not importend
                        path[child].append(child) #*not importend
                if not visited[child]:
                    visited[child] = True
            done_marks[node] = True

def dijkstra_mod_search(matrix, start, end, path_, nodes, depth, done_marks):
    if is_matrix(matrix) and depth >= 0:
        #init
        tmp_depth = depth
        n = len(matrix)
        visited = [False] * n
        queue = deque()
        marks = [inf] * n
        path = [[]] * n #*not importend
        #init node
        visited[start] = True
        marks[start] = 0
        queue.append(start)
        path[start].append(start) #*not importend
        while queue:
            node = queue.popleft()
            nodes.append(node)
            if node == end:
                return
            for child in get_children(matrix, node):
                if child not in path_ and child not in done_marks and (marks[node] + matrix[node][child]) < marks[child]:
                        marks[child] = marks[node] + matrix[node][child]
                        path[child] = [] #*not importend
                        path[child].extend(path[node]) #*not importend
                        path[child].append(child) #*not importend
                if depth > 0 and not visited[child] and child not in done_marks:
                    queue.append(child)
                    visited[child] = True
            done_marks.append(node)
            depth -= 1
        min_ = get_min_without_done(marks, done_marks)
        if min_ != 0:
            path_.extend(path[min_])
            dijkstra_mod_search(matrix, min_, end, path_, nodes, tmp_depth, done_marks)

def main():
    matrix1 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 10, 0, 39, 0],
        [0, 3, 0, 43, 0, 17, 65, 0, 0, 0],
        [0, 0, 43, 0, 3, 36, 0, 0, 0, 0],
        [0, 0, 0, 3, 0, 34, 0, 39, 0, 0],
        [0, 0, 17, 36, 34, 0, 32, 34, 0, 0],
        [0, 10, 65, 0, 0, 32, 0, 35, 67, 36],
        [0, 0, 0, 0, 39, 34, 35, 0, 0, 36],
        [0, 39, 0, 0, 0, 0, 67, 0, 0, 35],
        [0, 0, 0, 0, 0, 0, 36, 36, 35, 0]
    ]
    matrix = get_matrix_from_file('graph_data.xml')
    print('----Classic Dijkstra----')
    r = dijkstra_classic_search(matrix, 8, 4)
    print('Nodes: ' + str(r[0]))
    print('Path: ' + str(r[1]))
    sum_len = 0
    sum_path_crr = 0
    n = len(matrix)
    n1 = (n - 1) * (n - 1)
    for i in range(n):
        for j in range(n):
            cmp = list(compare_one(dijkstra_classic_search(matrix, i, j), dijkstra_classic_search(matrix, i, j)))
            sum_len += cmp[0]
            sum_path_crr += cmp[1]
    print('For all path:')
    print('Length: ' + str(sum_len/n1) + ' %')
    print('Errors: ' + str(sum_path_crr/n1) + ' %')
    print('----end----\n')


    print('----Dijkstra with priority----')
    r = dijkstra_priority_search(matrix, 8, 4)
    print('Nodes: ' + str(r[0]))
    print('Path: ' + str(r[1]))
    sum_len = 0
    sum_path_crr = 0
    n = len(matrix)
    n1 = (n - 1) * (n - 1)
    for i in range(n):
        for j in range(n):
            cmp = list(compare_one(dijkstra_classic_search(matrix, i, j), dijkstra_priority_search(matrix, i, j)))
            sum_len += cmp[0]
            sum_path_crr += cmp[1]
    print('For all path:')
    print('Length: ' + str(sum_len/n1) + ' %')
    print('Errors: ' + str(sum_path_crr/n1) + ' %')
    print('----end----\n')


    print('----Dijkstra with heuristic 1 function----')
    r = a_star(matrix, 8, 4,heuristic)
    print('Nodes: ' + str(r[0]))
    print('Path: ' + str(r[1]))
    sum_len = 0
    sum_path_crr = 0
    n = len(matrix)
    n1 = (n - 1) * (n - 1)
    for i in range(n):
        for j in range(n):
            cmp = list(compare_one(dijkstra_classic_search(matrix, i, j), a_star(matrix, i, j, heuristic)))
            sum_len += cmp[0]
            sum_path_crr += cmp[1]
    print('For all path:')
    print('Length: ' + str(sum_len/n1) + ' %')
    print('Errors: ' + str(sum_path_crr/n1) + ' %')
    print('----end----\n')

    print('----Dijkstra with heuristic 2 function----')
    r = a_star(matrix, 8, 4,heuristic2)
    print('Nodes: ' + str(r[0]))
    print('Path: ' + str(r[1]))
    sum_len = 0
    sum_path_crr = 0
    n = len(matrix)
    n1 = (n - 1) * (n - 1)
    for i in range(n):
        for j in range(n):
            cmp = list(compare_one(dijkstra_classic_search(matrix, i, j), a_star(matrix, i, j, heuristic2)))
            sum_len += cmp[0]
            sum_path_crr += cmp[1]
    print('For all path:')
    print('Length: ' + str(sum_len/n1) + ' %')
    print('Errors: ' + str(sum_path_crr/n1) + ' %')
    print('----end----\n')

    print('----Dijkstra with modification----')
    path = []
    nodes = []
    dijkstra_mod_search(matrix, 8, 4, path, nodes, 1, [])
    path = del_repeats(path)
    print('Nodes: ' + str(nodes))
    print('Path: ' + str(path))

    show_graph(matrix, path)

    sum_len = 0
    sum_path_crr = 0
    n = len(matrix)
    n1 = (n - 1) * (n - 1)
    for i in range(n):
        for j in range(n):
            path = []
            nodes = []
            dijkstra_mod_search(matrix, i, j, path, nodes, 1, [])
            path = del_repeats(path)
            if j not in path:
                path.append(j)
            cmp = list(compare_one(dijkstra_classic_search(matrix, i, j), [nodes, path]))
            sum_len += cmp[0]
            sum_path_crr += cmp[1]
    print('For all path:')
    print('Length: ' + str(sum_len/n1) + ' %')
    print('Errors: ' + str(sum_path_crr/n1) + ' %')
    print('----end----')

main()