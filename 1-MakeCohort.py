import pandas as pd
from datetime import datetime, timedelta
from Cohort.Cohort import Cohort

from Processing.Clean import clean_outcomes
from Processing.Clean import clean_blood
from Processing.Clean import clean_vitals
from Processing.Serialisation import jsonDump
from Processing.Settings import path

import sklearn

# 1. Creat the cohort
cohort_data = pd.read_csv(path+"original/outcomes.csv")
cohort_data = clean_outcomes(cohort_data)

cohort = Cohort(cohort_data, 'PatientID', "covid-KCH")

# 2. read Bloods
blood_data = pd.read_csv(path+"original/bloods.csv")
blood_data = clean_blood(blood_data)

# 2. read Vitals
vitals_data = pd.read_csv(path+"original/vitals.csv")
vitals_data = clean_vitals(vitals_data)

def main():
    ## 1. Adding bloods to the cohort
    patientIDs = set(cohort_data.PatientID)

    for idx in patientIDs:
        patientAdmissionDate = cohort_data.loc[cohort_data['PatientID']==idx].loc[:,'AdmitDate'].values[0]
        patientAdmissionDate = datetime.strptime(patientAdmissionDate, '%Y-%m-%d')

        startDate = patientAdmissionDate - timedelta(days=2)
        endDate = patientAdmissionDate + timedelta(days=3)

        bloods_for_patient = blood_data.loc[blood_data['patient_pseudo_id'] == idx]

        bloods_for_patient.columns = ['updatetime', 'basicobs_itemname_analysed', 'textualObs', 'basicobs_value_analysed',
                                      'basicobs_unitofmeasure', 'basicobs_referencelowerlimit',
                                      'basicobs_referenceupperlimit',
                                      'Unnamed: 0.1', 'patient_pseudo_id']

        bloods_for_patient['updatetime'] = pd.to_datetime(bloods_for_patient['updatetime'])
        dateMask = (bloods_for_patient['updatetime']>= startDate) & (bloods_for_patient['updatetime'] <= endDate)

        bloods_for_patient = bloods_for_patient.loc[dateMask]
        bloods_for_patient['updatetime'] = bloods_for_patient['updatetime'].astype(str)



        vitals_for_patient = vitals_data.loc[vitals_data['Patient_ID'] == idx]
        vitals_for_patient.columns = ['DateTime','Temperature','OxygenSaturation','RespirationRate','SupplementalOxygen','OxygenDelivery','OxygenLitres','HeartRate','SysBP','DiasBP','PainScore','GCSEye','GCSVerbal','GCSMotor','NEWS2','DateTimeRaw','Patient_ID']

        vitals_for_patient['DateTime'] = pd.to_datetime(vitals_for_patient['DateTime'])
        dateMask = (vitals_for_patient['DateTime'] >= startDate) & (vitals_for_patient['DateTime'] <= endDate)

        vitals_for_patient = vitals_for_patient.loc[dateMask]
        vitals_for_patient['DateTime']= vitals_for_patient['DateTime'].astype(str)

        if bloods_for_patient.shape[0] > 0 and vitals_for_patient.shape[0] > 0:
            cohort.addBloodObservations(idx, bloods_for_patient, patientAdmissionDate)
            cohort.addVitalsObservations(idx, vitals_for_patient, patientAdmissionDate)

    jsonDump(cohort,path+"Cohort.json")

if __name__ == "__main__":
    main()