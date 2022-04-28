import networkx as nx
import estimators
from graph_generators import *
import csv

################ U1
G1 = nx.random_tree(n=100, seed=0, create_using=nx.DiGraph)
G2 = nx.fast_gnp_random_graph(1000, 0.001, directed=True, seed = 0)
U=nx.DiGraph()
U.add_edges_from(G1.edges())
U.add_edges_from(G2.edges())

f_c = estimators.FormanRicci(U).compute_ricci_curvature_agg()
o_c = estimators.OllivierRicci(U, alpha=0.5, verbose="INFO").compute_ricci_curvature_agg()
s_c = estimators.SectionalEstimator(U).compute_sectional_curvature_agg()
print("\n *******(U1 graph)******* Forman curvature : ", f_c, ", Ollivier curvature : ", o_c, ", Sectional curvature : ", s_c)

################# U2
G1 = nx.random_tree(n=500, seed=0, create_using=nx.DiGraph)
G2 = nx.fast_gnp_random_graph(1000, 0.001, directed=True, seed = 0)
U=nx.DiGraph()
U.add_edges_from(G1.edges())
U.add_edges_from(G2.edges())
f_c = estimators.FormanRicci(U).compute_ricci_curvature_agg()
o_c = estimators.OllivierRicci(U, alpha=0.5, verbose="INFO").compute_ricci_curvature_agg()
s_c = estimators.SectionalEstimator(U).compute_sectional_curvature_agg()
print("\n *******(U2 graph)******* Forman curvature : ", f_c, ", Ollivier curvature : ", o_c, ", Sectional curvature : ", s_c)


#####################################################################################################
n = 1000
runs = 10
print("\n===== Number of nodes : =====", n)
curvs = {'forman' : [], 'sectional': [], 'ollivier' : []}
graphs = []

for i in range(runs):
    seed = random.randint(0, 10000000)
    T = Tree.generate(n, seed=seed, type='directed') #, rooted=True)
    DAG, count = SEQ_DAG.generate(T)
    #print("DAG, number of added edges", count)
    dag_with_cycles, count = SEQ_DAG_C.generate(DAG)
    #print("DAG with cycles, number of added edges", count)
    random_dg, count = SEQ_DG.generate(dag_with_cycles)
    DG2 = nx.fast_gnp_random_graph(1000, 0.0013, directed=True, seed = seed)
    DGB = nx.fast_gnp_random_graph(1000, 0.01, directed=True, seed = seed)

    graphs.append([T, DAG, dag_with_cycles, random_dg, DG2, DGB])

for idx, gg in enumerate(graphs):
    print('\n*************** Curvature estimation for run {} **************'.format(idx))

    forman_run_curvs = [estimators.FormanRicci(G).compute_ricci_curvature_agg() for G in gg]
    print("\n===== Forman-Ricci curvature : ", forman_run_curvs)
    curvs['forman'].append(forman_run_curvs)
    
    ollivier_run_curvs = []
    for G in gg:
        try:
            c = estimators.OllivierRicci(G, alpha=0.5, verbose="INFO").compute_ricci_curvature_agg()
            ollivier_run_curvs.append(c)
        except:
            ollivier_run_curvs.append(None)
    print("\n===== Ollivier-Ricci curvature : ", ollivier_run_curvs)
    curvs['ollivier'].append(ollivier_run_curvs)

    sectional_run_curvs = [estimators.SectionalEstimator(G).compute_sectional_curvature_agg() for G in gg]
    print("\n===== Sectional curvature ", sectional_run_curvs)
    curvs['sectional'].append(sectional_run_curvs)


#################### Saving computed curvatures to csv
for curv in ['forman', 'sectional', 'ollivier']:
    with open('curvs/curvs_{}.csv'.format(curv), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        data = list(map(list, zip(*curvs[curv])))
        writer.writerows(data)
