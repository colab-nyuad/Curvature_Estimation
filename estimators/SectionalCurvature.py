from shutil import copyfile
import numpy as np
import operator
from random import choice
from scipy.special import comb
import networkx as nx
from .util import logger, set_verbose

class SectionalEstimator:
    def __init__(self, G: nx.Graph,  verbose="ERROR"):
        if G.is_directed():
            self.G = G.to_undirected()
        else: 
            self.G = G
        set_verbose(verbose)

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
                    return np.mean(curvature)
                else:
                    return 0

            iter = iter + 1

            m = choice(nodes)
            ngh = list(C.neighbors(m))
            if len(ngh) < 2: continue

            b = choice(ngh)
            c = choice(ngh)
            if b == c: continue
        
            # sample reference node
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

        return np.mean(curvature)

    def compute_sectional_curvature(self):
        components = [self.G.subgraph(c) for c in nx.connected_components(self.G)]
        nodes = [c.number_of_nodes()**3 for c in components]
        total = np.sum(nodes)
        weights = [n/total for n in nodes]
        curvs = []

        for idx,c in enumerate(components):
            weight = weights[idx]
            n_samples = int(1000 * weight)
            nv = c.number_of_nodes()
            if nv < 4: 
                curvs.append(0)
                continue
            elif nv < 20:
                combs = comb(nv, 4)
                n_samples = combs if combs < n_samples or n_samples == 0 else n_samples
            curv = self.compute_component_curvature(c, n_samples)
            curvs.append(curv)

        return np.array(curvs), np.array(weights)

    def compute_sectional_curvature_agg(self):
        curvs, weights = self.compute_sectional_curvature()
        return np.sum(curvs * weights)


