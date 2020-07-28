import numpy as np

from MachineLearning.Models.LSTM import lstm_hyperparameter_tuning


#LSTM EXPERIMENT
class ExperimentV:
    def __init__(self,time_series):
        print(" IN EXPERIMENT IV. Columns of time series are:")
        print(time_series.columns)
        dynamic_features = ['Hour', 'ALT', 'Albumin', 'Blood Lactate', 'C-Reactive-Protein',
                            'Creatinine', 'D-Dimer',
                            'DiasBP', 'Estimated-GFR', 'Ferritin', 'FiO2', 'GCSMotor', 'GCSVerbal',
                            'Hb', 'HeartRate', 'INR',
                            'Lymphocytes', 'NEWS2',
                            'Neutrophils', 'OxygenLitres', 'OxygenSaturation',
                            'PCO2', 'PCV', 'PH', 'PLT', 'PO2', 'PO2/FIO2', 'PainScore',
                            'SupplementalOxygen', 'SysBP', 'Temperature', 'Troponin-T',
                            'Urea', 'WBC', 'cHCO3']


        experiment_number = "5"
        y = time_series['ITUAdmission7Days']
        y = y.astype(int)
        print(" CONVERSION SUCCESSFUL")
        print(y)
        outcome_label = "ITUAdmission7Days"
        X = time_series[dynamic_features]
        X.reset_index()
        groups = np.array(time_series['PatientID'])

        lstm_hyperparameter_tuning(X,y, outcome_label, groups, experiment_number)


