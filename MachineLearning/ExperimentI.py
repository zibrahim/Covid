import numpy as np
from MachineLearning.ExperimentalDesign import run_xgboost

class ExperimentI:
    def __init__(self,time_series, dynamic_features):
        experiment_number = "1"
        y = time_series['Mortality']
        X = time_series[dynamic_features]
        X.reset_index()
        groups = np.array(time_series['PatientID'])
        run_xgboost(X,y, groups, experiment_number)


