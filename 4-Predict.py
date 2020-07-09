import pandas as pd
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn import metrics
import matplotlib.pyplot as plt
import shap as sp
import lime as lm

from MachineLearning.ExperimentI import ExperimentI


from Processing.Settings import data_path

def main():
    time_series = pd.read_csv(data_path+"TimeSeriesAggregated.csv")
    dynamic_features = ['ALT', 'Albumin', 'Anticoagulant clinic INR', 'Bicarbonate',
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

    pd.options.mode.chained_assignment = None

    xgbm=xgb.XGBClassifier(scale_pos_weight=263/73,
                           learning_rate=0.007,
                           n_estimators=100,
                           gamma=0,
                           max_depth=4,
                           min_child_weight=2,
                           subsample=1,
                           eval_metric='error')
    rfm=RandomForestClassifier(n_estimators=100,
                               max_depth=4)
    lrm=LogisticRegression(solver='lbfgs')


    ExperimentI(time_series, dynamic_features, xgbm)
    #ExperimentII(x,y,xgbm,rfm,lrm)
    #ExperimentIII(x,y,rfm,lrm)
    #ExperimentIV(x,y,xgbm,rfm,lrm)
    #ExperimentV(x,y,xgbm,rfm,lrm)
    #ExperimentVI(x,y,xgbm,rfm,lrm)
    #ExperimentVII(xgbm,rfm,lrm)
    #ExperimentVIII(x,y,xgbm,rfm,lrm)

if __name__ == '__main__':
    main()
