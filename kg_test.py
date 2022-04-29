import estimators


datasets = ['WN18RR', 'FB15k-237', 'MetaQA_full', 'MetaQA_half']

for dataset in datasets:
    triples = []

    with open('{}/{}/triples.txt'.format('kg_data', dataset), 'r') as fin:
        data = fin.readlines()
        for d in data:
            triples.append(d.strip().split('\t'))

    c = estimators.KG_SectionalEstimator(triples).compute_sectional_curvature_agg()
    print("\n===== Sectional Curvature for {} : {} =====\n".format(dataset, c))
