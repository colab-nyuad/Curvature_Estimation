import networkx as nx
import matplotlib.pyplot as plt
import random
from networkx.algorithms.dag import *


class DirectedTree:
    #*******************************
    # Parameteres: n - number of nodes
    #*******************************

    def generate(n):
        G = nx.random_tree(n)
        H = nx.DiGraph([(u,v) for (u,v) in G.edges() if u<v])
        return H

class DAG:
    #*******************************
    # Parameteres: n - number of nodes
    #              p - Probability for edge creation, default : 1
    #              seed - random state (integer), default : None
    #*******************************
    
    def generate(n, p=1, seed=None):
        G = nx.fast_gnp_random_graph(n, p, directed=True, seed = seed)
        DAG = nx.DiGraph([(u, v) for (u, v) in G.edges() if u < v])
        return DAG

class ComleteGraph:
    #*******************************
    # Parameteres: n - number of nodes
    #              type - directed/undirected
    #*******************************

    def genearte(n, type='undericted'):
        if type == 'directed':
            G = nx.complete_graph(n, nx.DiGraph())
        else:
            G = nx.complete_graph(n)

class Graph:
    #*******************************
    # Parameteres: n - number of nodes
    #              p - Probability for edge creation, default : 1
    #              seed - random state (integer), default : None
    #              type - directed/undirected
    #*******************************

    def generate(n, p=1, seed=None, type = 'undirected'):
        directed = True if type == 'directed' else False
        G = nx.fast_gnp_random_graph(n, p, directed=directed, seed = seed)
        return G

class SpanningTree:
    #*******************************
    # Parameteres: n - number of nodes
    #              p - Probability for edge creation, default : 1
    #              seed - random state (integer), default : None
    #              type - directed/undirected
    #*******************************

    def generate(n, p=1, seed=None, type = 'undirected'):
        directed = True if type == 'directed' else False
        G = nx.fast_gnp_random_graph(n, p, directed=directed, seed = seed)
        T = nx.minimum_spanning_tree(G)
        return T
