import networkx as nx
import matplotlib.pyplot as plt
import random
from networkx.algorithms.dag import *
import numpy as np

class Tree:
    #*******************************
    # Parameteres: n - number of nodes
    #              seed - random state (integer), default : None
    #              type - directed/undirected
    #*******************************

    def generate(n, seed=None, type='undirected', rooted=True):
        G = nx.random_tree(n, seed=seed)

        if type == 'directed':
            if rooted:
                G = nx.random_tree(n=n, seed=seed, create_using=nx.DiGraph)
            else:
                G = nx.DiGraph([(u,v) for (u,v) in G.edges() if u<v])
        return G

class DAG:
    #*******************************
    # Parameteres: n - number of nodes
    #              p - Probability for edge creation, default : 0.5
    #              seed - random state (integer), default : None
    #*******************************
    
    def generate(n, p=0.5, seed=None):
        G = nx.fast_gnp_random_graph(n, p, directed=True, seed = seed)
        DAG = nx.DiGraph([(u, v) for (u, v) in G.edges() if u < v])
        return DAG

class ComleteGraph:
    #*******************************
    # Parameteres: n - number of nodes
    #              type - directed/undirected
    #*******************************

    def generate(n, type='undericted'):
        if type == 'directed':
            G = nx.complete_graph(n, nx.DiGraph())
        else:
            G = nx.complete_graph(n)

class Graph:
    #*******************************
    # Parameteres: n - number of nodes
    #              p - Probability for edge creation, default : 0.5
    #              seed - random state (integer), default : None
    #              type - directed/undirected
    #*******************************

    def generate(n, p=0.5, seed=None, type = 'undirected'):
        directed = True if type == 'directed' else False
        G = nx.fast_gnp_random_graph(n, p, directed=directed, seed = seed)
        return G

class SpanningTree:
    #*******************************
    # Parameteres: n - number of nodes
    #              p - Probability for edge creation, default : 0.5
    #              seed - random state (integer), default : None
    #              type - directed/undirected
    #*******************************

    def generate(n, p=0.5, seed=None, type = 'undirected'):
        directed = True if type == 'directed' else False
        G = nx.fast_gnp_random_graph(n, p, directed=directed, seed = seed)
        T = nx.minimum_spanning_tree(G)
        return T

class SEQ_DAG:
    #*******************************
    # Parameteres: T - nx.DiGraph (directed tree)
    #              number_of_edges_to_insert - number of edges to be added , default : 0.25
    #*******************************

    def generate(T, number_of_edges_to_insert=0.25):
        N = int(len(T.nodes)*number_of_edges_to_insert/2.)*2
        number_of_edges_tree = len(T.edges())
        DAG = T.copy()
        sample = random.sample(DAG.nodes, N)
        indexes = list(range(0, len(sample)))
        np.random.shuffle(indexes)
        pairs = {}
        for i in range(0, len(indexes), 2):
            pairs[sample[i]] = sample[i+1]

        for key, value in pairs.items():
            if key not in nx.descendants(DAG, value): #making sure no cycle will be formed
                DAG.add_edge(key, value)

        return DAG, len(DAG.edges()) - len(T.edges())


class SEQ_DAG_C:
    #*******************************
    # Parameteres: G - nx.DiGraph (DAG)
    #              number_of_edges_to_insert - number of edges to be added , default : 0.25
    #*******************************

    def generate(G, number_of_edges_to_insert=0.25):
        limit_edges = int(len(G.nodes) * number_of_edges_to_insert)
        N = int(len(G.nodes)/2.)*2
        DAG = G.copy()
        sample = random.sample(DAG.nodes, N)
        indexes = list(range(0, len(sample)))
        np.random.shuffle(indexes)
        pairs = {}
        for i in range(0, len(indexes), 2):
            pairs[sample[i]] = sample[i+1]
  
        count = 0
        for key, value in pairs.items():
            if key in nx.descendants(DAG, value):
                DAG.add_edge(key, value)
                count += 1
                if count > limit_edges: break

        return DAG, len(DAG.edges()) - len(G.edges())


class SEQ_DG:
    #*******************************
    # Parameteres: G - nx.DiGraph (DAG with cycles)
    #*******************************

    def generate(G):
        DG = G.copy()
        N = int(len(G.nodes)/2)
        sample = random.sample(G.edges, N)
        for i in sample:
            DG.remove_edge(i[0], i[1])
            DG.add_edge(i[1], i[0])
        return DG, len(DG.edges()) - len(G.edges())
