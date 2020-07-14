import numpy as np
from MachineLearning.ExperimentalDesign import run_xgboost_classifier

#INPUT: TIME SERIES WITH CLUSTERS ADDED
#OUTPUT: ITU ADMISSION
class ExperimentII:
    def __init__(self,time_series):
        dynamic_features = ['Hour', 'ALT', 'Albumin', 'Blood Lactate', 'C-Reactive-Protein',
                            'Creatinine', 'D-Dimer',
                            'DiasBP', 'Estimated-GFR', 'Ferritin', 'FiO2', 'GCSMotor', 'GCSVerbal',
                            'Hb', 'HeartRate', 'INR',
                            'Lymphocytes', 'NEWS2',
                            'Neutrophils', 'OxygenDelivery', 'OxygenLitres', 'OxygenSaturation',
                            'PCO2', 'PCV', 'PH', 'PLT', 'PO2', 'PO2/FIO2', 'PainScore',
                            'SupplementalOxygen', 'SysBP', 'Temperature', 'Troponin-T',
                            'Urea', 'WBC', 'cHCO3', 'cluster_assignment']

        experiment_number = "2"
        outcome_label = "ITUAdmission"
        y = time_series['ITUAdmission']
        X = time_series[dynamic_features]
        X.reset_index()
        groups = np.array(time_series['PatientID'])
        run_xgboost_classifier(X,y, outcome_label,  groups, experiment_number)

        outcome_label = "Mortality"
        y = time_series['Mortality']
        run_xgboost_classifier(X,y, outcome_label,  groups, experiment_number)


