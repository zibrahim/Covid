import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

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

        tprs = []
        aucs = []
        mean_fpr = np.linspace(0, 1, 100)
        plt.figure(figsize=(10, 10))

        for fold_ind, (training_ind, testing_ind) in enumerate(stratified_group_k_fold(X, y, groups, k=100)) :
            training_groups, testing_groups = groups[training_ind], groups[testing_ind]
            training_y, testing_y= y[training_ind], y[testing_ind]
            training_X, testing_X  = X.iloc[training_ind], X.iloc[testing_ind]

           # print("Training X", training_X['ALT'], "Training y", training_y)
           # print(type(training_groups), type(testing_groups))
            assert len(set(training_groups) & set(testing_groups)) == 0

            #Train, predict and Plot
            xgbm.fit(training_X, training_y)
            y_pred_rt = xgbm.predict_proba(testing_X)[:, 1]

            fpr, tpr, thresholds = roc_curve(testing_y, y_pred_rt)
            tprs.append(np.interp(mean_fpr, fpr, tpr))
            tprs[-1][0] = 0.0
            roc_auc = auc(fpr, tpr)
            aucs.append(roc_auc)
            plt.plot(fpr, tpr, lw=1, alpha=0.3,
                     label='ROC fold %d (AUC = %0.2f)' % (fold_ind, roc_auc))

            #add to the distribution dataframe, for verification purposes
            distrs.append(get_distribution(training_y))

            index.append(f'training set - fold {fold_ind}')
            distrs.append(get_distribution(testing_y))
            index.append(f'testing set - fold {fold_ind}')

        #Finallise ROC curve
        plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
                 label='Chance', alpha=.8)

        mean_tpr = np.mean(tprs, axis=0)
        mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)
        std_auc = np.std(aucs)
        plt.plot(mean_fpr, mean_tpr, color='b',
                 label=r'Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
                 lw=2, alpha=.8)

        std_tpr = np.std(tprs, axis=0)
        tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
        tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
        plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=.2,
                         label=r'$\pm$ 1 std. dev.')

        plt.xlim([-0.01, 1.01])
        plt.ylim([-0.01, 1.01])
        plt.xlabel('False Positive Rate', fontsize=18)
        plt.ylabel('True Positive Rate', fontsize=18)
        plt.title('Cross-Validation ROC of SVM', fontsize=18)
        #plt.legend(loc="lower right", prop={'size' : 15})
        plt.savefig("plots.pdf")

        distr_df = pd.DataFrame(distrs, index=index, columns=[f'Label {l}' for l in range(np.max(y) + 1)])
        distr_df.to_csv(stats_path+"Experiment1-K-Fold-Distributions.csv", index=True)
