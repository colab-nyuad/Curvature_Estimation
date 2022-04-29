from shutil import copyfile
import numpy as np
import operator
from random import choice
from scipy.special import comb
import networkx as nx
from .util import logger, set_verbose

#*****************************************************************************************************************************
#  Implementation for computing curvature from "Low-Dimensional Hyperbolic Knowledge Graph Embeddings"
#
#  Please note: - the points b,c are selected not from the direct neighbors of m (according to the description in the paper) 
#               - for componenets where we cannot sample any triangles we assume that the curvature is zero
#               - these components are counted in the weighted average
#
#*****************************************************************************************************************************

class KG_SectionalEstimator:
    def __init__(self, triples: list,  verbose="ERROR"):
        set_verbose(verbose)
        self.entity2idx = {}
        self.rel2idx = {}
        self.triples = []

        for triple in triples:
            if triple[0] not in self.entity2idx:
                self.entity2idx[triple[0]] = len(self.entity2idx)
            if triple[2] not in self.entity2idx:
                self.entity2idx[triple[2]] = len(self.entity2idx) 
            if triple[1] not in self.rel2idx:
                self.rel2idx[triple[1]] = len(self.rel2idx)
            self.triples.append([self.entity2idx[triple[0]], self.rel2idx[triple[1]], self.entity2idx[triple[2]]])
        
        self.idx2entity = {v:k for k,v in self.entity2idx.items()}
        self.idx2rel = {v:k for k,v in self.rel2idx.items()}
        
        logger.trace("Entities and relation maps created")

    def compute_component_curvature(self, C, n_samples):
        nodes = list(C)
        nodes.sort()
        curvature = []
        max_iter = 1000
        iter = 0
        idx = 0

        while idx < n_samples:

            # if in max_iter we cannot sample return curvature
            if iter == max_iter:
                if len(curvature) > 0:
                    return curvature
                else:
                    return [0]

            iter = iter + 1

            b = choice(nodes)
            c = choice(nodes)
            if b == c: continue
            try:
                bc_nodes = nx.shortest_path(C, source=b, target=c)
            except nx.NetworkXNoPath:
                continue
            
            l = len(bc_nodes)
            if l % 2 == 0:
                continue
            m = bc_nodes[l//2]
            a = choice([l for l in nodes if l not in [m,b,c]])

            try:
                bc = len(nx.shortest_path(C, source=b, target=c)) - 1
                ab = len(nx.shortest_path(C, source=a, target=b)) - 1
                ac = len(nx.shortest_path(C, source=a, target=c)) - 1
                am = len(nx.shortest_path(C, source=a, target=m)) - 1
                iter = 0

            except nx.NetworkXNoPath:
                continue

            curv = (am**2 + bc**2/4 - (ab**2 + ac**2) / 2) / (2 * am)
            curvature.append(curv)
            
            idx = idx + 1

        return curvature

    def compute_sectional_curvature(self):
        # Span graph by relations 
        triples_per_relation = {}
        for triple in self.triples:
            if triple[1] not in triples_per_relation:
                triples_per_relation[triple[1]] = nx.Graph()
            triples_per_relation[triple[1]].add_edge(triple[0], triple[2])

        nodes_gr = []
        curvs_gr = []

        for tr, Gr in triples_per_relation.items():
            components = [Gr.subgraph(c) for c in nx.connected_components(Gr)]
            nodes = [c.number_of_nodes()**3 for c in components]
            total = np.sum(nodes)
            weights = [n/total for n in nodes]
            curvs = []

            for idx,c in enumerate(components):
                weight = weights[idx]
                n_samples = int(1000 * weight)
                nv = c.number_of_nodes()
                if nv < 4: # we cannot sample from components if there are less than 4 nodes
                    curvs.extend([0])
                    continue
                elif nv < 20: # to balance if the graph is higly disconnected or weight of the component is too small 
                    combs = comb(nv, 4)
                    n_samples = combs if combs < n_samples or n_samples == 0 else n_samples
                curv = self.compute_component_curvature(c, n_samples)
                curvs.extend(curv)
            
            c = np.mean(curvs)
            print(self.idx2rel[tr], c)
            curvs_gr.append(c)
            nodes_gr.append(total)

        return np.array(curvs_gr), np.array(nodes_gr)

    def compute_sectional_curvature_agg(self):
        curvs, nodes = self.compute_sectional_curvature()
        return np.sum(curvs * nodes) / np.sum(nodes)


