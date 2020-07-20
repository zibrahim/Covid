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

    clustered_cohort_deltatwodays = pd.read_csv(clustering_path + "ClusteredDataFirst2Days.csv")
    clustered_cohort_deltatwodays = clustered_cohort_deltatwodays[['PatientID',
                                                                   'NEWSBaseline',
                                                                   'CReactiveProteinBaseline',
                                                                   'SysBPBaseline',
                                                                   'DiasBPBaseline',
                                                                   'WBCBaseline',
                                                                   'LymphocytesBaseline',
                                                                   'NeutrophilsBaseline',
                                                                   'PLTBaseline',
                                                                   'UreaBaseline',
                                                                   'CreatinineBaseline',
                                                                   'HbBaseline',
                                                                   'AlbuminBaseline',
                                                                   'Age',
                                                                   'SxToAdmit',
                                                                   'ITUAdmission7Days',
                                                                   'ITUAdmission14Days',
                                                                   'ITUAdmission30Days',
                                                                   'Mortality7Days',
                                                                   'Mortality14Days',
                                                                   'Mortality30Days',
                                                                   'NumComorbidities',
                                                                   'cluster_assignment']]
    timeseries = timeseries.drop(['OrdinalHour','FourHourIndex','ITUAdmission','ITUAdmission7Days',
                     'ITUAdmission14Days','ITUAdmission30Days','Day','Mortality',
                     'Mortality7Days','Mortality14Days','Mortality30Days','Age', 'SxToAdmit', 'NumComorbidities'], axis=1)

    timeseries_clustered_deltatwodays= pd.merge(timeseries, clustered_cohort_deltatwodays, on=['PatientID'])

    cols = list(timeseries_clustered_deltatwodays)

    cols.insert(2, cols.pop(cols.index('AlbuminBaseline')))
    cols.insert(2, cols.pop(cols.index('HbBaseline')))
    cols.insert(2, cols.pop(cols.index('PLTBaseline')))
    cols.insert(2, cols.pop(cols.index('UreaBaseline')))
    cols.insert(2, cols.pop(cols.index('CreatinineBaseline')))
    cols.insert(2, cols.pop(cols.index('NeutrophilsBaseline')))
    cols.insert(2, cols.pop(cols.index('LymphocytesBaseline')))
    cols.insert(2, cols.pop(cols.index('WBCBaseline')))
    cols.insert(2, cols.pop(cols.index('DiasBPBaseline')))
    cols.insert(2, cols.pop(cols.index('SysBPBaseline')))
    cols.insert(2, cols.pop(cols.index('CReactiveProteinBaseline')))
    cols.insert(2, cols.pop(cols.index('NEWSBaseline')))
    cols.insert(2, cols.pop(cols.index('cluster_assignment')))
    cols.insert(2, cols.pop(cols.index('Age')))
    cols.insert(2, cols.pop(cols.index('SxToAdmit')))
    cols.insert(2, cols.pop(cols.index('NumComorbidities')))
    cols.insert(1, cols.pop(cols.index('ITUAdmission7Days')))
    cols.insert(1, cols.pop(cols.index('ITUAdmission14Days')))
    cols.insert(1, cols.pop(cols.index('ITUAdmission30Days')))
    cols.insert(1, cols.pop(cols.index('Mortality7Days')))
    cols.insert(1, cols.pop(cols.index('Mortality14Days')))
    cols.insert(1, cols.pop(cols.index('Mortality30Days')))

    #timeseries_clustered_deltatwodays = timeseries_clustered_deltatwodays.ix[:, cols]
    timeseries_clustered_deltatwodays  = timeseries_clustered_deltatwodays.loc[:, cols]

    timeseries_clustered_deltatwodays.to_csv(clustered_timeseries_path +"TimeSeriesAggregatedClusteredDeltaTwoDays.csv", index=False)



if __name__ == '__main__' :
    main()
