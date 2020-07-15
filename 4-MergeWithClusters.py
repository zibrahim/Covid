import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn import metrics
import matplotlib.pyplot as plt
import shap as sp
import lime as lm



from Processing.Settings import data_path, clustering_path, clustered_timeseries_path

def main():
    #Clustering based on demographics
    timeseries = pd.read_csv(data_path + "TimeSeriesAggregated.csv")
    clustered_cohort_demographics = pd.read_csv(clustering_path + "ClusteredDataDemographics.csv")
    clustered_cohort_demographics = clustered_cohort_demographics[['PatientID', 'NumComorbiditiesUnscaled', 'cluster_assignment']]
    timeseries_clustered_demographics = pd.merge(timeseries, clustered_cohort_demographics, on=['PatientID'])
    timeseries_clustered_demographics.to_csv(clustered_timeseries_path +"TimeSeriesAggregatedClustered.csv", index=False)

    #Clustering based on demographics only <= 75 years of age
    clustered_cohort_demographics_notold = pd.read_csv(clustering_path + "ClusteredDataDemographicsNotOld.csv")
    clustered_cohort_demographics_notold = clustered_cohort_demographics_notold[['PatientID', 'NumComorbidities', 'cluster_assignment']]
    timeseries_clustered_demographics_notold = pd.merge(timeseries, clustered_cohort_demographics_notold, on=['PatientID'])
    timeseries_clustered_demographics_notold.to_csv(clustered_timeseries_path +"TimeSeriesAggregatedClusteredNotOld.csv", index=False)

    #Clustering using baseline measurements for patients
    clustered_cohort_baseline = pd.read_csv(clustering_path + "ClusteredDataBaseline.csv")
    clustered_cohort_baseline = clustered_cohort_baseline[['PatientID', 'NumComorbidities', 'cluster_assignment']]
    timeseries_clustered_baseline = pd.merge(timeseries, clustered_cohort_baseline, on=['PatientID'])
    timeseries_clustered_baseline.to_csv(clustered_timeseries_path +"TimeSeriesAggregatedClusteredBaseline.csv", index=False)


    clustered_cohort_deltatwodays = pd.read_csv(clustering_path + "ClusteredDataFirst2Days.csv")
    clustered_cohort_deltatwodays = clustered_cohort_deltatwodays[['PatientID', 'cluster_assignment']]
    timeseries_clustered_deltatwodays= pd.merge(timeseries, clustered_cohort_deltatwodays, on=['PatientID'])
    timeseries_clustered_deltatwodays.to_csv(clustered_timeseries_path +"TimeSeriesAggregatedClusteredDeltaTwoDays.csv", index=False)



if __name__ == '__main__' :
    main()
