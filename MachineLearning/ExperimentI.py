import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics

#from sklearn.model_selection import GroupKFold

from Processing.Settings import stats_path
from MachineLearning.ExperimentalDesign import stratified_group_k_fold, get_distribution

class ExperimentI:
    def __init__(self,time_series, dynamic_features, xgbm):

        groups = np.array(time_series['PatientID'])

        y = time_series['Mortality']
        X = time_series[dynamic_features]
        X.reset_index()

        distrs = [get_distribution(y)]
        index = ['Entire set']

        for fold_ind, (training_ind, testing_ind) in enumerate(stratified_group_k_fold(X, y, groups, k=100)) :
            training_groups, testing_groups = groups[training_ind], groups[testing_ind]
            training_y, testing_y= y[training_ind], y[testing_ind]
            training_X, testing_X  = X.iloc[training_ind], X.iloc[testing_ind]

           # print("Training X", training_X['ALT'], "Training y", training_y)
           # print(type(training_groups), type(testing_groups))
            assert len(set(training_groups) & set(testing_groups)) == 0


            #Train, predict and Plot
            fig, ax = plt.subplots(1, 1, figsize=(10, 10))
            xgbm = xgbm.fit(training_X, training_y)
            y_pred = xgbm.predict_proba(testing_X)[:, 1]
            fpr, tpr, threshold = metrics.roc_curve(testing_y, y_pred)
            roc_auc = metrics.auc(fpr, tpr)
            plt.plot(fpr, tpr, 'r', label='XGBoost (AUC:%0.3F)' % roc_auc, linestyle='-')
            plt.legend(loc='lower right', frameon=False)
            plt.savefig("plots.pdf")


            #add to the distribution dataframe, for verification purposes
            distrs.append(get_distribution(training_y))

            index.append(f'training set - fold {fold_ind}')
            distrs.append(get_distribution(testing_y))
            index.append(f'testing set - fold {fold_ind}')


        distr_df = pd.DataFrame(distrs, index=index, columns=[f'Label {l}' for l in range(np.max(y) + 1)])
        distr_df.to_csv(stats_path+"Experiment1-K-Fold-Distributions.csv", index=True)
