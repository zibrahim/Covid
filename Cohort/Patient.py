import pandas as pd
import datetime

class Patient:
    def __init__(self, id, age,gender, sxDate, admitDate, deathDate, itudate,
                 ethnicity, copd, asthma, hf, diabetes, ihd, htn, ckd):
        self.Patient_id = id
        self.Age = age
        self.Gender = gender
        self.SxDate = sxDate
        self.AdmitDate = admitDate
        self.DeathDate = deathDate
        self.ITUDate = itudate
        self.Ethnicity = ethnicity
        self.COPD = copd
        self.Asthma = asthma
        self.HF = hf
        self.Diabetes = diabetes
        self.IHD = ihd
        self.HTN = htn
        self.CKD = ckd
        self.observations = []

    def addObservations( self, observations ):
        for o in observations:
            self.observations.append(o)

    def printString( self ):
        print(" Patient: ", self.Patient_id, self.Age, self.Gender)

    def printObservationVolume( self ):
        print(" Patient: ", self.Patient_id," has: ", len(self.observations), "observations")

    def getNumberOfObservations( self ):
        return len(self.observations)

    def as_dict(self):
        number_comorbidities = self.CKD+self.HTN+self.IHD+self.Diabetes+self.HF+self.Asthma+self.COPD
        AdmitDate = datetime.datetime.strptime(self.AdmitDate, '%Y-%m-%d')
        SxDate = datetime.datetime.strptime(self.SxDate, '%Y-%m-%d')
        symptomsToAdmission = AdmitDate - SxDate
        mortality = 0
        if not (pd.isnull(self.DeathDate)):
            mortality = 1
        ituAdmission = 0
        if not (pd.isnull(self.ITUDate)):
            ituAdmission = 1
        patient_row = {'PatientID' : self.Patient_id,
                       'Age' : self.Age,
                       'Gender' : self.Gender,
                       'SxDate' : self.SxDate,
                       'AdmitDate' : self.AdmitDate,
                       'DeathDate' : self.DeathDate,
                       'ITUDate' : self.ITUDate,
                       'Ethnicity' : self.Ethnicity,
                       'COPD' : self.COPD,
                       'Asthma' : self.Asthma,
                       'HF' : self.HF,
                       'Diabetes' : self.Diabetes,
                       'IHD' : self.IHD,
                       'HTN' : self.HTN,
                       'CKD' : self.CKD,
                       'NumComorbidities' : number_comorbidities,
                       'Mortality':mortality,
                       'ITUAdmission': ituAdmission,
                       'SymptomsToAdmission': symptomsToAdmission
                       }
        return patient_row