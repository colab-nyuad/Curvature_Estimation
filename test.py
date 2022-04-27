import networkx as nx
import estimators
from graph_generators import *

n = 1000
seed = 147321
print("\n===== Number of nodes : =====", n)

T = Tree.generate(n, type='directed', rooted=True)
print("Directed Tree, number of edges", len(T.edges()))
DAG, count = SEQ_DAG.generate(T)
print("DAG, number of added edges", count)
dag_with_cycles, count = SEQ_DAG_C.generate(DAG)
print("DAG with cycles, number of added edges", count)
random_dg, count = SEQ_DG.generate(dag_with_cycles)
print("Directed Graph, number of added edges", count)

graphs = {'Directed rooted Tree': T,
          'DAG' : DAG,
          'DAG with added cycles' : dag_with_cycles, 
          'Random Directed Graph' : random_dg}

for name, G in graphs.items():
    print('\n*************** Curvature estimation for {} **************'.format(name))
    
    frc = estimators.FormanRicci(G)
    c = frc.compute_ricci_curvature_agg()
    print("\n===== Forman-Ricci curvature : ", c)

#    orc = estimators.OllivierRicci(G, alpha=0.5, verbose="INFO")
#    c = orc.compute_ricci_curvature_agg()
#    print("\n===== Ollivier-Ricci curvature : ", c)

    sec = estimators.SectionalEstimator(G)
    c = sec.compute_sectional_curvature_agg()
    print("\n===== Sectional curvature ", c)


