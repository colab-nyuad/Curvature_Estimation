import os
import sys
sys.path.append('../contrib/hyperbolics/pytorch')
sys.path.append('../contrib/hyperbolics')
import networkx as nx
import numpy as np
import math
import torch
import logging



class GlobalCurvature:
    def __init__(self, G, loss='distortion'):
        self.G = G

    def compute_global_curvature(iter=1000, laerning_rate=0.001):

G = nx.convert_node_labels_to_integers(sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0])

common_params = dict(
    batch_size=65536,
    epochs=iters,
    checkpoint_freq=100,
    resample_freq=2000,
    lazy_generation=True,
    subsample=1024,
    riemann=True,
    burn_in=0,
    learning_rate=lr,
    log_level=logging.ERROR,
    use_adagrad=True,
    reduce_lr_on_plateu=False,
    reluloss=False
)

for loss in losses:

        if loss=="zero_one":
            common_params["reluloss"] = True

        dist_curvature, pearson_curvature = get_grad_desc_curvature_v2(G, common_params, dimensionality)
        if loss=="zero_one":
            curv = pearson_curvature
        else:
            curv = dist_curvature


        curvatures_to_test = [curv]

        common_params["learning_rate"] = first_lr
        curvature2metrics1 = get_curvature2metrics(curvatures_to_test, G, common_params, dimensionality)



def get_grad_desc_curvature_v2(G, common_params, dimensionality):
    best_dist = None
    best_dist_curvature = None
    best_zero_one = None
    best_zero_one_curvature = None
    
    for space_name, space_params in get_space_params(dim).items():
        emb, stat = learn_emb(G, learn_scale=True, **space_params, **common_params)
        if space_name == 'euc':
            dist_scale = 1
            zero_one_scale = 1
        else:
            dist_scale = float(stat['Best-dist-scale'])
            zero_one_scale = float(stat['Best-zero-one-scale'])

        dist_curvature = scale2curvature(space_name, dist_scale, dim)
        zero_one_curvature = scale2curvature(space_name, zero_one_scale, dim)

        assert(stat["Final-loss"] != "nan")
        dist = float(stat["Best-dist"])
        zero_one = float(stat["Best-zero-one"])

        if best_dist is None or dist < best_dist:
            best_dist_curvature = dist_curvature
            best_dist = dist

        if best_zero_one is None or zero_one < best_zero_one:
            best_zero_one_curvature = zero_one_curvature
            best_zero_one = zero_one

    return best_dist_curvature, best_zero_one_curvature


def get_curvature2metrics(curvatures, G, common_params, dimensionality):
    curvature2metrics = {}
    print("space\tscale\tcurvature\tdist\tpearson\tzero_one")
    space_params = get_space_params(dimensionality)
    for curvature in curvatures:
        space_name, scale = curvature2space_and_scale(curvature, dimensionality)
        try:
            emb, stat = learn_emb(
                G,
                learn_scale=False,
                initial_space_scale=math.log(scale),
                **space_params[space_name],
                **common_params
            )
            distortion = float(stat["Best-dist"])
            zero_one = float(stat["Best-zero-one"])
        except:
            print("Error: cannot learn embedding")
            distortion = 10000.
            pearson = -1.
            zero_one = 1.
        curvature2metrics[curvature] = {'distortion': distortion, 'zero_one': zero_one}
    return curvature2metrics

