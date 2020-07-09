import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold

from Processing.Settings import path
from MachineLearning.ExperimentalDesign import stratified_group_k_fold, get_distribution

class ExperimentI:
    def __init__(self,time_series, dynamic_features):

        groups = groups = np.array(time_series['PatientID'])
        y = time_series['Mortality']
        X = time_series[dynamic_features]

        distrs = [get_distribution(y)]
        index = ['training set']

        for fold_ind, (dev_ind, val_ind) in enumerate(stratified_group_k_fold(X, y, groups, k=5)) :
            dev_y, val_y = y[dev_ind], y[val_ind]
            dev_groups, val_groups = groups[dev_ind], groups[val_ind]

            assert len(set(dev_groups) & set(val_groups)) == 0

            distrs.append(get_distribution(dev_y))
            index.append(f'development set - fold {fold_ind}')
            distrs.append(get_distribution(val_y))
            index.append(f'validation set - fold {fold_ind}')

        print('Distribution per class:')
        x = pd.DataFrame(distrs, index=index, columns=[f'Label {l}' for l in range(np.max(y) + 1)])
        x.to_csv("distributions.csv", index=False)
