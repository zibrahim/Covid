import pandas as pd
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn import metrics
import matplotlib.pyplot as plt
import shap as sp
import lime as lm
from tqdm import tqdm


from Processing.Settings import path


def main():

    pd.options.mode.chained_assignment = None
    timeseries_dataset=pd.read_csv(path+"TimeSeriesAggregated.csv")
    patientsNotOld = pd.read_csv(path+"PatientsNotOld.csv")

    patient_ids_not_old = patientsNotOld['PatientID']
    timeseries_dataset = timeseries_dataset[timeseries_dataset.PatientID.isin(patient_ids_not_old) ]

    #oxygenation_index_missingness = timeseries_dataset['PO2/FIO2'].isnull().sum()*100/len(timeseries_dataset['PO2/FIO2'])

    patient_clusters = patientsNotOld[['PatientID', 'cluster_assignment']]

    timeseries_with_clusters = pd.merge(timeseries_dataset, patient_clusters, on='PatientID', how='inner')

    timeseries_with_clusters.to_csv(path+"timeseries_with_clusters_not_old.csv", index=False)

   #print(timeseries_with_clusters[timeseries_with_clusters['Mortality'] ==1])


    xgbm=xgb.XGBClassifier(scale_pos_weight=263/73,
                           learning_rate=0.007,
                           n_estimators=100,
                           gamma=0,
                           max_depth=4,
                           min_child_weight=2,
                           subsample=1,
                           eval_metric='error')
    rfm=RandomForestClassifier(n_estimators=100,
                               max_depth=4)
    lrm=LogisticRegression(solver='lbfgs')


    #ExperimentI(x,y,xgbm,rfm,lrm)
    #ExperimentII(x,y,xgbm,rfm,lrm)
    #ExperimentIII(x,y,rfm,lrm)
    #ExperimentIV(x,y,xgbm,rfm,lrm)
    #ExperimentV(x,y,xgbm,rfm,lrm)
    #ExperimentVI(x,y,xgbm,rfm,lrm)
    #ExperimentVII(xgbm,rfm,lrm)
    #ExperimentVIII(x,y,xgbm,rfm,lrm)

if __name__ == '__main__':
    main()
