import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn import metrics
import matplotlib.pyplot as plt
import shap as sp
import lime as lm

from MachineLearning.ExperimentI import ExperimentI


from Processing.Settings import data_path

def main():
    aggregated_timeseries = pd.read_csv(data_path + "TimeSeriesAggregated.csv")
    clustered_cohort = pd.read_csv(data_path + "cohortClustered.csv")
    clustered_cohort_not_old = pd.read_csv(data_path + "cohortClusteredNotOld.csv")

    print(clustered_cohort.columns)
    clustered_cohort = clustered_cohort[['PatientID', 'NumComorbiditiesUnscaled', 'cluster_assignment']]
    clustered_cohort_not_old = clustered_cohort_not_old[['PatientID', 'NumComorbiditiesUnscaled', 'cluster_assignment']]

    print(aggregated_timeseries.shape)
    print(clustered_cohort.shape)
    print(clustered_cohort_not_old.shape)

    #print(aggregated_timeseries.PatientID)
    #print(clustered_cohort.PatientID)

    aggregated_timeseries_all = pd.merge(aggregated_timeseries, clustered_cohort, on=['PatientID'])
    aggregated_timeseries_not_old = pd.merge(aggregated_timeseries, clustered_cohort_not_old, on=['PatientID'])

    print(" COLUMN NAMES OF AGGREGARED TIME SERIES ALL OLD: ")
    print(aggregated_timeseries_all.columns)
    print(aggregated_timeseries_not_old.shape)

    aggregated_timeseries_all.to_csv(data_path+"TimeSeriesAggregatedClustered.csv", index=False)
    aggregated_timeseries_not_old.to_csv(data_path+"TimeSeriesAggregatedClusteredNotOld.csv", index=False)


if __name__ == '__main__' :
    main()
