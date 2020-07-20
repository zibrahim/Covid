from datetime import datetime
import numpy as np
import pandas as pd

from Cohort.Patient import Patient
from Cohort.Observation import Observation
from Processing.Utils import binSearch


class Cohort :
    def __init__ ( self, cohort_df=pd.DataFrame(), IDField='', title="") :
        self.name = title
        self.individuals = []
        self.individual_ids = []

        if len(IDField)> 0:
            unique_ids = np.sort(cohort_df[IDField].unique())

            for some_id in list(unique_ids):
                individual = Patient(cohort_df.loc[cohort_df['PatientID'] == some_id].loc[:,'PatientID'].values[0],
                                 cohort_df.loc[cohort_df['PatientID'] == some_id].loc[:, 'Age'].values[0],
                                 cohort_df.loc[cohort_df['PatientID'] == some_id].loc[:, 'Gender'].values[0],
                                 cohort_df.loc[cohort_df['PatientID'] == some_id].loc[:, 'SxDate'].values[0],
                                 cohort_df.loc[cohort_df['PatientID'] == some_id].loc[:, 'AdmitDate'].values[0],
                                 cohort_df.loc[cohort_df['PatientID'] == some_id].loc[:, 'DeathDate'].values[0],
                                 cohort_df.loc[cohort_df['PatientID'] == some_id].loc[:, 'ITUDate'].values[0],
                                 cohort_df.loc[cohort_df['PatientID'] == some_id].loc[:, 'Ethnicity'].values[0],
                                 cohort_df.loc[cohort_df['PatientID'] == some_id].loc[:, 'COPD'].values[0],
                                 cohort_df.loc[cohort_df['PatientID'] == some_id].loc[:, 'Asthma'].values[0],
                                 cohort_df.loc[cohort_df['PatientID'] == some_id].loc[:, 'HF'].values[0],
                                 cohort_df.loc[cohort_df['PatientID'] == some_id].loc[:, 'Diabetes'].values[0],
                                 cohort_df.loc[cohort_df['PatientID'] == some_id].loc[:, 'IHD'].values[0],
                                 cohort_df.loc[cohort_df['PatientID'] == some_id].loc[:, 'HTN'].values[0],
                                 cohort_df.loc[cohort_df['PatientID'] == some_id].loc[:, 'CKD'].values[0])
                self.individuals.append(individual)
                self.individual_ids.append(some_id)


    def addIndividual(self,p, pid ):
        self.individuals.append(p)
        self.individual_ids.append(pid)

    def addObservationsToIndividual( self, ids, observations ):
        i = binSearch(self.individual_ids, ids)
        self.individuals[i].addObservations(observations)

    def addBloodObservations (self, pid, bloods_for_patient, patientAdmissionDate ) :
        observations = []
        for index, row in bloods_for_patient.iterrows() :
            if not pd.isnull(row.basicobs_value_analysed) :
                obs = Observation("Blood",
                                  row.basicobs_itemname_analysed,
                                  datetime.strptime(row.updatetime, '%Y-%m-%d %H:%M:%S') - patientAdmissionDate,
                                  row.basicobs_value_analysed,
                                  row.basicobs_unitofmeasure,
                                  row.textualObs)

                observations.append(obs)
        self.addObservationsToIndividual(pid, observations)

    def addVitalsObservations( self, pid, vital_for_patient, patientAdmissionDate ) :
        observations = []
        for index, row in vital_for_patient.iterrows() :
            Temperature = row.Temperature
            if not pd.isnull(Temperature) :
                obs = Observation("Vital", "Temperature",
                                  datetime.strptime(row.DateTime, '%Y-%m-%d %H:%M:%S') - patientAdmissionDate,
                                  Temperature,  # column value
                                  "",  # unit of measurement - not applicable to vitals, or get later
                                  ""  # textual observation not available for vitals
                                  )
                observations.append(obs)

            OxygenSaturation = row.OxygenSaturation
            if not pd.isnull(OxygenSaturation) :
                obs = Observation("Vital", "OxygenSaturation",
                                  datetime.strptime(row.DateTime, '%Y-%m-%d %H:%M:%S') - patientAdmissionDate,
                                  OxygenSaturation,  # column value
                                  "",  # unit of measurement - not applicable to vitals, or get later
                                  ""  # textual observation not available for vitals
                                  )
                observations.append(obs)

            RespirationRate = row.RespirationRate
            if not pd.isnull(RespirationRate) :
                obs = Observation("Vital", "RespirationRate",
                                  datetime.strptime(row.DateTime, '%Y-%m-%d %H:%M:%S') - patientAdmissionDate,
                                  RespirationRate,  # column value
                                  "",  # unit of measurement - not applicable to vitals, or get later
                                  ""  # textual observation not available for vitals
                                  )
                observations.append(obs)

            SupplementalOxygen = row.SupplementalOxygen
            if not SupplementalOxygen == -1 :
                obs = Observation("Vital", "SupplementalOxygen",
                                  datetime.strptime(row.DateTime, '%Y-%m-%d %H:%M:%S') - patientAdmissionDate,
                                  SupplementalOxygen,  # column value
                                  "",  # unit of measurement - not applicable to vitals, or get later
                                  ""  # textual observation not available for vitals
                                  )
                observations.append(obs)

            OxygenDelivery = row.OxygenDelivery
            if not OxygenDelivery == -1 :
                obs = Observation("Vital", "OxygenDelivery",
                                  datetime.strptime(row.DateTime, '%Y-%m-%d %H:%M:%S') - patientAdmissionDate,
                                  OxygenDelivery,  # column value
                                  "",  # unit of measurement - not applicable to vitals, or get later
                                  ""  # textual observation not available for vitals
                                  )
                observations.append(obs)

            OxygenLitres = row.OxygenLitres
            if not pd.isnull(OxygenLitres) :
                obs = Observation("Vital", "OxygenLitres",
                                  datetime.strptime(row.DateTime, '%Y-%m-%d %H:%M:%S') - patientAdmissionDate,
                                  OxygenLitres,  # column value
                                  "",  # unit of measurement - not applicable to vitals, or get later
                                  ""  # textual observation not available for vitals
                                  )
                observations.append(obs)

            HeartRate = row.HeartRate
            if not pd.isnull(HeartRate) :
                obs = Observation("Vital", "HeartRate",
                                  datetime.strptime(row.DateTime, '%Y-%m-%d %H:%M:%S') - patientAdmissionDate,
                                  HeartRate,  # column value
                                  "",  # unit of measurement - not applicable to vitals, or get later
                                  ""  # textual observation not available for vitals
                                  )
                observations.append(obs)

            SysBP = row.SysBP
            if not pd.isnull(SysBP) :
                obs = Observation("Vital", "SysBP",
                                  datetime.strptime(row.DateTime, '%Y-%m-%d %H:%M:%S') - patientAdmissionDate,
                                  SysBP,  # column value
                                  "",  # unit of measurement - not applicable to vitals, or get later
                                  ""  # textual observation not available for vitals
                                  )
                observations.append(obs)

            DiasBP = row.DiasBP
            if not pd.isnull(DiasBP) :
                obs = Observation("Vital", "DiasBP",
                                  datetime.strptime(row.DateTime, '%Y-%m-%d %H:%M:%S') - patientAdmissionDate,
                                  DiasBP,  # column value
                                  "",  # unit of measurement - not applicable to vitals, or get later
                                  ""  # textual observation not available for vitals
                                  )
                observations.append(obs)

            PainScore = row.PainScore
            if not pd.isnull(PainScore) :
                obs = Observation("Vital", "PainScore",
                                  datetime.strptime(row.DateTime, '%Y-%m-%d %H:%M:%S') - patientAdmissionDate,
                                  PainScore,  # column value
                                  "",  # unit of measurement - not applicable to vitals, or get later
                                  ""  # textual observation not available for vitals
                                  )
                observations.append(obs)

            GCSEye = row.GCSEye
            if not pd.isnull(GCSEye) :
                obs = Observation("Vital", "GCSEye",
                                  datetime.strptime(row.DateTime, '%Y-%m-%d %H:%M:%S') - patientAdmissionDate,
                                  GCSEye,  # column value
                                  "",  # unit of measurement - not applicable to vitals, or get later
                                  ""  # textual observation not available for vitals
                                  )
                observations.append(obs)

            GCSVerbal = row.GCSVerbal
            if not pd.isnull(GCSVerbal) :
                obs = Observation("Vital", "GCSVerbal",
                                  datetime.strptime(row.DateTime, '%Y-%m-%d %H:%M:%S') - patientAdmissionDate,
                                  GCSVerbal,  # column value
                                  "",  # unit of measurement - not applicable to vitals, or get later
                                  ""  # textual observation not available for vitals
                                  )
                observations.append(obs)

            GCSMotor = row.GCSMotor
            if not pd.isnull(GCSMotor) :
                obs = Observation("Vital", "GCSMotor",
                                  datetime.strptime(row.DateTime, '%Y-%m-%d %H:%M:%S') - patientAdmissionDate,
                                  GCSMotor,  # column value
                                  "",  # unit of measurement - not applicable to vitals, or get later
                                  ""  # textual observation not available for vitals
                                  )
                observations.append(obs)

            NEWS2 = row.NEWS2
            if not pd.isnull(NEWS2) :
                obs = Observation("Vital", "NEWS2",
                                  datetime.strptime(row.DateTime, '%Y-%m-%d %H:%M:%S') - patientAdmissionDate,
                                  NEWS2,  # column value
                                  "",  # unit of measurement - not applicable to vitals, or get later
                                  ""  # textual observation not available for vitals
                                  )
                observations.append(obs)

        self.addObservationsToIndividual(pid, observations)


    def clean( self ):
        remove_indices = []
        length = len(self.individuals)
        for i in range(length) :
            if len(getattr(self.individuals[i], 'observations')) == 0:
                remove_indices.append(i)

        for index in sorted(remove_indices, reverse=True) :
            del self.individuals[index]

    def getAllColumnNames( self ):

        all_column_names = [o.Name for p in self.individuals for o in p.observations]

        all_column_names = np.unique(all_column_names)

        all_column_names = np.insert(all_column_names, 0,"SxToAdmit")
        all_column_names = np.insert(all_column_names, 0,"NumComorbidities")

        all_column_names = np.insert(all_column_names, 0,"Mortality30Days")
        all_column_names = np.insert(all_column_names, 0,"Mortality")
        all_column_names = np.insert(all_column_names, 0,"ITUAdmission")
        all_column_names = np.insert(all_column_names, 0,"Hour")
        all_column_names = np.insert(all_column_names, 0,"Age")
        all_column_names = np.insert(all_column_names, 0,"PatientID")

        return all_column_names