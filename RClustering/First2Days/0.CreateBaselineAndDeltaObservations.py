import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

from Processing.CleanTimeSeries import remove_alpha
from Processing.Settings import data_path, clustering_path
from Processing.Utils import getDay

def main():
    #Vitals:
    # 'C-Reactive-Protein', 'SysBP', 'DiasBP', 'HeartRate'
    #Already in NEWS: Temperature, 'OxygenSaturation', 'RespirationRate'
    #Bloods:
    # 'WBC', 'Lymphocytes', 'Neutrophils', 'Platelets', 'Urea', 'Creatinine', 'C-Reactive-Protein', 'Hb', 'Albumin'

    time_series = pd.read_csv(data_path+"TimeSeries.csv")
    time_series['SxToAdmit'] = [getDay(x) for x in time_series['SxToAdmit']]

    time_series = time_series[time_series.Hour > -24]
    time_series = time_series[time_series.Hour <= 48]

    time_series.iloc[:, 7:(len(time_series.columns) - 1)] = remove_alpha(time_series.iloc[:, 7:(len(time_series.columns) - 1)])

    time_series['PatientID2'] = time_series['PatientID']

    ObsFirst = time_series[['PatientID', 'PatientID2', 'NEWS2', 'C-Reactive-Protein', 'SysBP', 'DiasBP','WBC',
                            'Lymphocytes','Neutrophils','PLT','Urea','Creatinine','Hb',
                            'Albumin', 'FiO2',  'PO2/FIO2']].groupby('PatientID2').first()


    ObsFirst[['NEWS2', 'C-Reactive-Protein', 'SysBP', 'DiasBP','WBC','Lymphocytes','Neutrophils','PLT',
              'Urea','Creatinine','Hb','Albumin', 'FiO2',  'PO2/FIO2']]= ObsFirst[['NEWS2',
                                                              'C-Reactive-Protein', 'SysBP', 'DiasBP',
                                                              'WBC','Lymphocytes','Neutrophils',
                                                              'PLT','Urea','Creatinine',
                                                              'Hb','Albumin', 'FiO2',  'PO2/FIO2']].astype(float)
    ObsFirst.columns = ['PatientID', 'NEWSBaseline',  'CReactiveProteinBaseline', 'SysBPBaseline',
                        'DiasBPBaseline','WBCBaseline','LymphocytesBaseline','NeutrophilsBaseline',
                        'PLTBaseline', 'UreaBaseline', 'CreatinineBaseline', 'HbBaseline',
                        'AlbuminBaseline', 'FiO2Baseline',  'PO2/FIO2Baseline']

    ObsLast = time_series[['PatientID', 'PatientID2', 'NEWS2', 'C-Reactive-Protein', 'SysBP',
                           'DiasBP', 'WBC', 'Lymphocytes','Neutrophils', 'PLT', 'Urea',
                           'Creatinine', 'Hb', 'Albumin', 'FiO2',  'PO2/FIO2']].groupby('PatientID2').last()

    ObsLast[['NEWS2', 'C-Reactive-Protein', 'SysBP', 'DiasBP', 'WBC', 'Lymphocytes', 'Neutrophils',
                 'PLT','Urea', 'Creatinine', 'Hb', 'Albumin', 'FiO2',  'PO2/FIO2']]= ObsLast[['NEWS2',
                                                                        'C-Reactive-Protein',
                                                                         'SysBP', 'DiasBP', 'WBC',
                                                                         'Lymphocytes', 'Neutrophils', 'PLT',
                                                                         'Urea','Creatinine',
                                                                         'Hb', 'Albumin',
                                                                        'FiO2',  'PO2/FIO2']].astype(float)
    ObsLast.columns = ['PatientID', 'NEWSLast', 'CReactiveProteinLast', 'SysBPLast', 'DiasBPLast', 'WBCLast',
                       'LymphocytesLast', 'NeutrophilsLast', 'PLTLast', 'UreaLast', 'CreatinineLast',
                       'HbLast', 'AlbuminLast', 'FiO2Last',  'PO2/FIO2Last']

    Obs = pd.merge(ObsFirst, ObsLast, on=['PatientID'])
    Obs['DeltaNEWS'] = Obs['NEWSLast'] - Obs['NEWSBaseline']
    Obs['DeltaCReactiveProtein'] = Obs['CReactiveProteinLast'] - Obs['CReactiveProteinBaseline']
    Obs['DeltaSysBP'] = Obs['SysBPLast'] - Obs['SysBPBaseline']
    Obs['DeltaDiasBP'] = Obs['DiasBPLast'] - Obs['DiasBPBaseline']
    Obs['DeltaWBC'] = Obs['WBCLast'] - Obs['WBCBaseline']
    Obs['DeltaLymphocytes'] = Obs['LymphocytesLast'] - Obs['LymphocytesBaseline']
    Obs['DeltaNeutrophils'] = Obs['NeutrophilsLast'] - Obs['NeutrophilsBaseline']
    Obs['DeltaPLT'] = Obs['PLTLast'] - Obs['PLTBaseline']
    Obs['DeltaUrea'] = Obs['UreaLast'] - Obs['UreaBaseline']
    Obs['DeltaCreatinine'] = Obs['CreatinineLast'] - Obs['CreatinineBaseline']
    Obs['DeltaHb'] = Obs['HbLast'] - Obs['HbBaseline']
    Obs['DeltaAlbumin'] = Obs['AlbuminLast'] - Obs['AlbuminBaseline']
    Obs['DeltaFiO2'] = Obs['FiO2Last'] - Obs['FiO2Baseline']
    Obs['DeltaPO2/FIO2'] = Obs['PO2/FIO2Last'] - Obs['PO2/FIO2Baseline']

    #missingness = (aggregate_series.isnull().sum() * 100 /len(aggregate_series))
    Obs.reindex(Obs.columns)
    Obs = Obs.loc[:, pd.notnull(Obs).sum()>len(Obs)*.80]

    #Impute missing values as SOM clustering does not accommodate missingness
    imp = IterativeImputer(max_iter=10, random_state=0)
    imp.fit(Obs.iloc[:,7:])
    Obs.iloc[:,7:] = imp.transform(Obs.iloc[:,7:])

    demographics_outcomes  = time_series[['PatientID', 'Age', 'SxToAdmit',
                                          'ITUAdmission3Days', 'ITUAdmission5Days',
                                          'ITUAdmission7Days','ITUAdmission14Days',
                                          'ITUAdmission30Days',
                                          'Mortality3Days', 'Mortality5Days',
                                          'Mortality7Days', 'Mortality14Days',
                                          'Mortality30Days',
                                          'NumComorbidities']]

    Obs = pd.merge(Obs, demographics_outcomes, on=['PatientID'])


    Obs['PatientID2'] = Obs['PatientID']
    Obs = Obs.groupby(['PatientID2']).first()

    Obs.to_csv(clustering_path+"BaselineAndDeltaObs.csv", index=False)
if __name__ == "__main__" :
    main()