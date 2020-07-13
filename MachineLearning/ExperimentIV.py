import numpy as np
from MachineLearning.ExperimentalDesign import run_xgboost_classifier

#INPUT: TIME SERIES WITH CLUSTERS BASED ON BASELINE MEASUREMENTS OF VITALS
#OUTPUT: OUTCOME: MORTALITY
class ExperimentIV:
    def __init__(self,time_series):
        print(" IN EXPERIMENT IV. Columns of time series are:")
        print(time_series.columns)
        dynamic_features = ['Age','Hour', 'ALT', 'Albumin', 'Blood Lactate', 'C-Reactive-Protein',
                            'Creatinine', 'D-Dimer',
                            'DiasBP', 'Estimated-GFR', 'Ferritin', 'FiO2', 'GCSMotor', 'GCSVerbal',
                            'Hb', 'HeartRate', 'INR',
                            'Lymphocytes', 'NEWS2',
                            'Neutrophils', 'OxygenDelivery', 'OxygenLitres', 'OxygenSaturation',
                            'PCO2', 'PCV', 'PH', 'PLT', 'PO2', 'PO2/FIO2', 'PainScore',
                            'SupplementalOxygen', 'SysBP', 'Temperature', 'Troponin-T',
                            'Urea', 'WBC', 'cHCO3', 'NumComorbidities', 'cluster_assignment']

        experiment_number = "4"
        y = time_series['ITUAdmission']
        X = time_series[dynamic_features]
        X.reset_index()
        groups = np.array(time_series['PatientID'])
        run_xgboost_classifier(X,y, groups, experiment_number)


