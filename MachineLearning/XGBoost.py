import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import xgboost as xgb

from Processing.Settings import stats_path, prediction_path
from MachineLearning.MLSetup import get_distribution, stratified_group_k_fold

def run_xgboost_classifier(X,y, label, groups, experiment_number):
    xgbm=xgb.XGBClassifier(scale_pos_weight=263/73,
                           learning_rate=0.007,
                           n_estimators=100,
                           gamma=0,
                           max_depth=4,
                           min_child_weight=2,
                           subsample=1,
                           eval_metric='error')

    y = y.astype(int)
    distrs = [get_distribution(y)]
    index = ['Entire set']

    tprs = []
    aucs = []
    mean_fpr = np.linspace(0, 1, 10) #CROSS VALIDATION CHANGE
    plt.figure(figsize=(10, 10))

    for fold_ind, (training_ind, testing_ind) in enumerate(stratified_group_k_fold(X, y, groups, k=10)) : #CROSS-VALIDATION
        training_groups, testing_groups = groups[training_ind], groups[testing_ind]
        training_y, testing_y = y[training_ind], y[testing_ind]
        training_X, testing_X = X.iloc[training_ind], X.iloc[testing_ind]

        # print("Training X", training_X['ALT'], "Training y", training_y)
        # print(type(training_groups), type(testing_groups))
        assert len(set(training_groups) & set(testing_groups)) == 0

        # Train, predict and Plot
        xgbm.fit(training_X, training_y)
        y_pred_rt = xgbm.predict_proba(testing_X)[:, 1]

        fpr, tpr, thresholds = roc_curve(testing_y, y_pred_rt)
        tprs.append(np.interp(mean_fpr, fpr, tpr))
        tprs[-1][0] = 0.0
        roc_auc = auc(fpr, tpr)
        aucs.append(roc_auc)
        plt.plot(fpr, tpr, lw=1, alpha=0.3,
                 label='ROC fold %d (AUC = %0.2f)' % (fold_ind, roc_auc))

        # add to the distribution dataframe, for verification purposes
        distrs.append(get_distribution(training_y))

        index.append(f'training set - fold {fold_ind}')
        distrs.append(get_distribution(testing_y))
        index.append(f'testing set - fold {fold_ind}')

    # Finallise ROC curve
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
    plt.title('XGBoost Cross-Validation ROC', fontsize=18)
    # plt.legend(loc="lower right", prop={'size' : 15})

    plt.savefig(prediction_path + "Experiment"+ experiment_number+ label + "ROC_XGBoost.pdf")

    distr_df = pd.DataFrame(distrs, index=index, columns=[f'Label {l}' for l in range(np.max(y) + 1)])
    distr_df.to_csv(stats_path + "Experiment"+experiment_number+"-K-Fold-Distributions.csv", index=True)
