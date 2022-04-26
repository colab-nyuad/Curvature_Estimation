import networkx as nx
import estimators
from graph_generators import *
from GraphRicciCurvature.FormanRicci import FormanRicci


n = 200
p = 0.7
seed = 190
print("\n===== Number of nodes : =====", n)

graphs = {'Directed Tree': DirectedTree.generate(n),
          'DAG' : DAG.generate(n, p=p, seed=seed),
          'Directed Graph' : Graph.generate(n, p=p, seed=seed, type='direct')}

for name, G in graphs.items():
    print('\n*************** Curvature estimation for {} **************'.format(name))
    #print("\n===== Compute the Forman-Ricci curvature of the given graph G =====")
    #frc = estimators.FormanRicci(G, method='1d')
    #c = frc.compute_ricci_curvature_agg()
    #print("\n===== Value 1d: {} ======".format(c))
    #frc = estimators.FormanRicci(G, method='augmented')
    #c = frc.compute_ricci_curvature_agg()
    #print("\n===== Value 1d: {} ======".format(c))

    # Forman-Ricci for direct graph 
    
    Gd = nx.DiGraph()
    Gd.add_edges_from([(0, 9),(0, 7),(0, 6),(0, 1), (1, 2), (1, 3), (1, 4),(1, 5)])
    print("\n===== Compute the Forman-Ricci curvature of the given directed graph Gd =====")
    frc_directed = FormanRicci(Gd)
    frc_directed.compute_ricci_curvature()
    for n1, n2 in frc_directed.G.edges():
        print("Directed Graph: The Forman-Ricci curvature of edge(%d,%d) id %f" %
              (n1, n2, frc_directed.G[n1][n2]["formanCurvature"]))

    print("\n===== Compute the Ollivier-Ricci curvature of the given graph G =====")
    orc = estimators.OllivierRicci(G, alpha=0.5, verbose="INFO")
    c = orc.compute_ricci_curvature_agg()
    print("\n===== Value: {} ======".format(c))

    print("\n===== Compute Sectional curvature of the given graph G =====")
    sec = estimators.SectionalEstimator(G)
    c = sec.compute_sectional_curvature_agg()
    print("\n===== Value: {} ======".format(c))


