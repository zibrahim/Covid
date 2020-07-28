import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import IterativeImputer
from sklearn.linear_model import LogisticRegression
from MachineLearning.MLSetup import scale

from MachineLearning.Experiments.ExperimentV import ExperimentV

from Processing.Settings import data_path, clustered_timeseries_path

def main():
    time_series_clustered_demographics = pd.read_csv(clustered_timeseries_path +"TimeSeriesAggregatedClustered.csv")
    time_series_clustered_demographics_not_old = pd.read_csv(clustered_timeseries_path+"TimeSeriesAggregatedClusteredNotOld.csv")
    time_series_clustered_baseline = pd.read_csv(clustered_timeseries_path+"TimeSeriesAggregatedClusteredBaseline.csv")
    time_series_clustered_twodays = pd.read_csv(clustered_timeseries_path+"TimeSeriesAggregatedClusteredDeltaTwoDays.csv")
    time_series = pd.read_csv(data_path+"TimeSeriesAggregated.csv")


    dynamic_features = ['Hour','ALT', 'Albumin', 'Anticoagulant clinic INR', 'Bicarbonate',
           'Biochemistry (Glucose)', 'Blood Lactate', 'C-Reactive-Protein',
           'CSF Glucose', 'Creatinine', 'Creatinine Clearance.', 'D-Dimer',
           'DiasBP', 'Estimated-GFR', 'Fasting Glucose.', 'Ferritin', 'FiO2',
           'Fluid Albumin.', 'Fluid Glucose.', 'GCSEye', 'GCSMotor', 'GCSVerbal',
           'HBA1c-DCCT', 'HBA1c-IFCC', 'Hb', 'HbA1c', 'HeartRate', 'INR',
           'Lactate', 'Lactate (CSF)', 'Lactate (plasma)', 'Lactate-Dehydrogenase',
           'Lymphocytes', 'Lymphocytes (LYMP)', 'NEWS2', 'NT-pro-BNP',
           'Neutrophils', 'OxygenDelivery', 'OxygenLitres', 'OxygenSaturation',
           'PCO2', 'PCV', 'PH', 'PLT', 'PO2', 'PO2/FIO2', 'PainScore',
           'Protein/Creatinine Ratio', 'Random Glucose:', 'Random Urine pH',
           'Random-Urine-Creatinine', 'RespirationRate', 'Reticulocyte HB Content',
           'SupplementalOxygen', 'SysBP', 'Temperature', 'Troponin-I',
           'Troponin-T', 'U-albumin/creat. ratio', 'Urea', 'Urine Albumin conc.',
           'Urine Glucose', 'Urine Urea', 'Venous Bicarbonate', 'Venous PCO2',
           'Venous PO2', 'Venous pH', 'WBC', 'WBC count (CSF)',
           'WBC count (Fluid)', 'cHCO3']


    rfm=RandomForestClassifier(n_estimators=100,
                               max_depth=4)
    lrm=LogisticRegression(solver='lbfgs')


    #ExperimentI(time_series_clustered_demographics)
    #ExperimentII(time_series_clustered_demographics_not_old)
    #ExperimentIII(time_series_clustered_baseline)
    #ExperimentIV(time_series_clustered_twodays)

    dynamic_features = ['Hour', 'ALT', 'Albumin', 'Blood Lactate', 'C-Reactive-Protein',
                        'Creatinine', 'D-Dimer',
                        'DiasBP', 'Estimated-GFR', 'Ferritin', 'FiO2', 'GCSMotor', 'GCSVerbal',
                        'Hb', 'HeartRate', 'INR',
                        'Lymphocytes', 'NEWS2',
                        'Neutrophils', 'OxygenLitres', 'OxygenSaturation',
                        'PCO2', 'PCV', 'PH', 'PLT', 'PO2', 'PO2/FIO2', 'PainScore',
                        'SupplementalOxygen', 'SysBP', 'Temperature', 'Troponin-T',
                        'Urea', 'WBC', 'cHCO3']

    imp = IterativeImputer(max_iter=10, random_state=0)
    imp.fit(time_series[dynamic_features])
    time_series[dynamic_features] = imp.transform(time_series[dynamic_features])

    time_series = scale(time_series, dynamic_features)
    ExperimentV(time_series)
    #ExperimentVI(x,y,xgbm,rfm,lrm)
    #ExperimentVII(xgbm,rfm,lrm)
    #ExperimentVIII(x,y,xgbm,rfm,lrm)

if __name__ == '__main__':
    main()
