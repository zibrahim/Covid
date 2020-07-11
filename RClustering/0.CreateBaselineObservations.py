import pandas as pd
import os
from Processing.Dictionaries import aggregation
from Processing.Helpers import getDay
from Processing.CleanTimeSeries import remove_alpha
from Processing.CleanTimeSeries import merge_INR
from Processing.Settings import data_path
def main():
    time_series = pd.read_csv(data_path+"TimeSeries.csv")
    time_series['PatientID2'] = time_series['PatientID']
    print(time_series.columns)
    aggregate_series = time_series.groupby('PatientID2').first()

    aggregate_series.to_csv(data_path+"BaselineObservations.csv", index=False)
if __name__ == "__main__" :
    main()