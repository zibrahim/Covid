import pandas as pd
import os
from Processing.Dictionaries import aggregation
from Processing.Helpers import getDay
from Processing.CleanTimeSeries import remove_alpha
from Processing.CleanTimeSeries import merge_INR
from Processing.Settings import data_path
def main():
    time_series = pd.read_csv(data_path+"TimeSeries.csv")

    time_series['SxToAdmit']  = [getDay(ox) for ox in  time_series ['SxToAdmit']]

    time_series.to_csv(data_path+"TimeSeriesNotAggregated.csv", index=False)

    time_series = merge_INR(time_series)
    time_series = remove_alpha(time_series)
    #time_series = remove_nacolumns(time_series)
    patient_ids = time_series['PatientID'].unique()

    #2. Create a new column, call it FourHourIndex
    time_series['FourHourIndex'] = -1
    new_time_series = pd.DataFrame(columns=time_series.columns)

    #3. Create a new column that aggregates every 4 hours into 1
    for p in patient_ids:
        patient_slice = time_series.loc[time_series.PatientID ==p,]
        patient_slice.reset_index()

        lower_limit = 0
        upper_limit = 3
        flag = False

        while (flag == False):
            if upper_limit >= len(patient_slice.index) :
                flag = True
                patient_slice.iloc[lower_limit:len(patient_slice.index),patient_slice.columns.get_loc('FourHourIndex')] = lower_limit

            else:
                patient_slice.iloc[lower_limit:upper_limit+1,patient_slice.columns.get_loc('FourHourIndex')] = lower_limit

            lower_limit = lower_limit + 4
            upper_limit = upper_limit + 4

        new_time_series = new_time_series.append(patient_slice, ignore_index=True)
    new_time_series.to_csv(data_path+"new_time_series.csv", index=False)

    new_time_series = pd.read_csv(data_path+"new_time_series.csv")
    os.remove(data_path+"new_time_series.csv")

    new_time_series[["PatientID"]] = "p_"+new_time_series[["PatientID"]].astype(str)

    int_columns = [ "Day", "Hour", 'ITUAdmission', "Age", "Mortality","Mortality30Days","NumComorbidities", "SxToAdmit","OrdinalHour", "FourHourIndex"]
    new_time_series[int_columns] = new_time_series[int_columns].astype(int)

    na_columns = set(new_time_series.columns) - set(int_columns)
    na_columns = na_columns - set(['PatientID'])

    float_columns = new_time_series.columns[7:]
    new_time_series[float_columns] = new_time_series[float_columns].astype(float)

    aggregate_series = new_time_series.groupby(['PatientID', 'FourHourIndex']).aggregate(aggregation)
    print(aggregate_series['PO2/FIO2'].isnull().sum() * 100 /len(aggregate_series['PO2/FIO2']))
    # 1. Identify columns where PO2/FIO2 is null but both FIO2 and PO2 are not null
    matches = aggregate_series['PO2/FIO2'].isnull() & aggregate_series['FiO2'].notnull() & aggregate_series['PO2'].notnull()
    # 2. Calculate PO2/FIO2 for the columns using the individual PO2 and FIO2 values
    aggregate_series.loc[matches, 'PO2/FIO2'] = aggregate_series.loc[matches, 'PO2']/aggregate_series.loc[matches, 'FiO2']

    #print(aggregate_series['PO2/FIO2'].isnull().sum() * 100 /len(aggregate_series['PO2/FIO2']))

    #print("dim before remove na ", aggregate_series.shape)
    aggregate_series = aggregate_series.dropna(subset = na_columns, how='all')
    #print("dim after remove na ", aggregate_series.shape)
    aggregate_series.to_csv(data_path+"TimeSeriesAggregated.csv", index=False)
if __name__ == "__main__" :
    main()