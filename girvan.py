import networkx as nx
import numpy as np
import copy
import sys


def get_input(input_path):
    n = eval(open(input_path).readline().rstrip())
    graph = nx.from_numpy_matrix(np.loadtxt(input_path, skiprows = 1, dtype = int))
    return n, graph

def cal_betweenness(G):
    betweenness = {edge:0 for edge in G.edges}
    #compute the betweenness by working up the tree
    for u in G.nodes():
        bfs_graph = bfs(u, graph)
        for e in bfs_graph.edges:
            betweenness[e] += bfs_graph.edges[e]['flow']/2

    return betweenness

def cal_moduality(G, m, A):
    Q = 0
    A = A.toarray()
    for g in nx.connected_components(G):
        for i in g:
            for j in g:
                Q += A[i][j] - (np.sum(A[i]) * np.sum(A[j])/(2 * m))

    return Q/ (2 * m)

def bfs(root, G):
    G = copy.deepcopy(G)
    
    #Initialization
    nx.set_node_attributes(G, 0, 'pvalue')
    nx.set_node_attributes(G, -1, 'level')
    nx.set_node_attributes(G, None, 'parents')
    nx.set_edge_attributes(G, 0, 'flow')
    nx.set_node_attributes(G, 1, 'flow')

    #bfs core part
    queue = [root]
    level = 1
    G.nodes[root]['level'] = 0
    G.nodes[root]['pvalue'] = 1
    while queue:
        new_queue = []
        for v in queue:
            for u in G.nodes:
                if G.has_edge(u, v):
                    if G.nodes[u]['level'] == -1:
                        G.nodes[u]['level'] = level
                        G.nodes[u]['parents'] = []
                        G.nodes[u]['parents'].append(v)
                        G.nodes[u]['pvalue'] += G.nodes[v]['pvalue']
                        new_queue.append(u)
                    elif G.nodes[u]['level'] > G.nodes[v]['level']:
                        G.nodes[u]['parents'].append(v)
                        G.nodes[u]['pvalue'] += G.nodes[v]['pvalue']
        queue = new_queue
        level += 1

    #compute node flow
    while level > 0:
        for u in G.nodes:
            if (G.nodes[u]['level'] == level):
                for p in G.nodes[u]['parents']:
                    G.edges[u,p]['flow'] = G.nodes[u]['flow'] * G.nodes[p]['pvalue']/G.nodes[u]['pvalue']
                    G.nodes[p]['flow'] += G.edges[u,p]['flow']
        level -= 1

    return G

def remove_edges(G, betweenness):
    edges = []
    max = 0
    for k,v in betweenness.items():
        if v > max:
            max = v
            edges.clear()
            edges.append(k)
        elif v == max:
            edges.append(k)

    for e in edges:
        G.remove_edge(*e)

def girvan(n, G):
    m = len(G.edges)
    A = nx.adjacency_matrix(G)
    decomposition_history = []
    Q_history = []
    while(nx.number_connected_components(G) != n):
        betweenness = cal_betweenness(G)
        remove_edges(G, betweenness)
        decomposition_history.append(tuple(list(g) for g in nx.connected_components(G)))
        Q_history.append(cal_moduality(G, m, A))

    return decomposition_history, Q_history

def ans_output(decomposition_history, Q_history):
    f = open("output.txt", "w")

    print("network decomposition")
    f.write("network decomposition\n")
    for i in decomposition_history:
        print(i)
        f.write(str(i) + '\n')

    max_Q = 0
    max_index = 0
    for i in range(0, len(Q_history)):
        if (len(decomposition_history[i]) > 1):
            print("{} {} : modularity {:.4f}".format(len(decomposition_history[i]), "clusters", Q_history[i]))
            f.write("{} {} : modularity {:.4f}\n".format(len(decomposition_history[i]), "clusters", Q_history[i]))
        else:
            print("{} {} : modularity {:.4f}".format(len(decomposition_history[i]), "cluster", Q_history[i]))
            f.write("{} {} : modularity {:.4f}\n".format(len(decomposition_history[i]), "cluster", Q_history[i]))
        if Q_history[i] > max_Q:
            max_Q = Q_history[i]
            max_index = i

    print("optimal structure : {}".format(decomposition_history[max_index]))
    f.write("optimal structure : {}\n".format(decomposition_history[max_index]))

    f.close()

if __name__ == '__main__':
    input_path = sys.argv[1]
    n, graph = get_input(input_path)
    decomposition_history, Q_history = girvan(n, graph)
    ans_output(decomposition_history, Q_history)
