import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

from Processing.CleanTimeSeries import remove_alpha
from Processing.Settings import data_path, clustering_path


def main():
    time_series = pd.read_csv(data_path+"TimeSeries.csv")
    print("original dim", time_series.shape)
    time_series = time_series[time_series.Hour < 25]

    time_series.iloc[:, 7:(len(time_series.columns) - 1)] = remove_alpha(time_series.iloc[:, 7:(len(time_series.columns) - 1)])

    time_series['PatientID2'] = time_series['PatientID']
    print(time_series.columns)
    #print(time_series.columns)
    aggregate_series = time_series.groupby('PatientID2').first()

    missingness = (aggregate_series.isnull().sum() * 100 /len(aggregate_series))
    missingness.reindex(aggregate_series.columns)


    aggregate_series = aggregate_series.loc[:, pd.notnull(aggregate_series).sum()>len(aggregate_series)*.80]

    #Impute missing values as SOM clustering does not accommodate missingness
    imp = IterativeImputer(max_iter=10, random_state=0)
    imp.fit(aggregate_series.iloc[:,7:])
    aggregate_series.iloc[:,7:] = imp.transform(aggregate_series.iloc[:,7:])
    aggregate_series.to_csv(clustering_path+"BaselineObservations.csv", index=False)
if __name__ == "__main__" :
    main()