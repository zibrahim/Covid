import json
import datetime

import numpy as np
import pandas as pd
from Cohort.Patient import Patient
from Cohort.Observation import Observation
from Processing.Serialisation import CohortEncoder
from Processing.Helpers import BinSearch

class Cohort :
    def __init__ ( self, cohort_df, IDField) :
        self.individuals = []
        self.individual_ids = []
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

    def addObservationsToIndividual( self, ids, observations ):
        i = BinSearch(self.individual_ids, ids)
        self.individuals[i].addObservations(observations)

    def addBloodObservations (self, pid, bloods_for_patient, patientAdmissionDate ) :
        observations = []
        for index, row in bloods_for_patient.iterrows() :
            if not pd.isnull(row.basicobs_value_analysed) :  # and (
                #    datetime.strptime(row.updatetime, '%Y-%m-%d %H:%M:%S') - patientAdmissionDate) > timedelta(seconds=0) :
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
            # if (datetime.strptime(row.DateTime, '%Y-%m-%d %H:%M:%S') - patientAdmissionDate) > timedelta(seconds=0) :
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

    def printCohort ( self ) :
        print("")
        for ind in self.individuals:
            ind.printObservationVolume()

    def writeToDataFrame( self ):
        patient_list = self.individuals
        PatientDF = pd.DataFrame([x.as_dict() for x in patient_list])

        ObservationDF = pd.DataFrame()
        for ind in self.individuals:
            observation_list = getattr(ind, 'observations')
            ObservationDFOnePatient = pd.DataFrame([x.as_dict(getattr(ind,'Patient_id')) for x in observation_list])
            ObservationDF = ObservationDF.append((ObservationDFOnePatient))

        PatientDF.to_csv("/Users/babylon/Documents/Covid-19/Data/Patients.csv", index=False)
        ObservationDF.to_csv("/Users/babylon/Documents/Covid-19/Data/Observations.csv", index=False)

    def getAllColumnNames( self ):
        all_column_names = [o.Name for p in self.individuals for o in p.observations]
        all_column_names = np.unique(all_column_names)
        all_column_names = np.insert(all_column_names, 0,"SxToAdmit")
        all_column_names = np.insert(all_column_names, 0,"Mortality")
        all_column_names = np.insert(all_column_names, 0,"ITUAdmission")
        all_column_names = np.insert(all_column_names, 0,"Hour")
        all_column_names = np.insert(all_column_names, 0,"PatientID")

        print(" All Columns: ", all_column_names)
        return all_column_names

    def jsonDump( self ):
        j = ""
        for ind in self.individuals:
            person_dic = ind.as_dict()
            i = 0
            for obs in ind.__getattribute__("observations"):
                person_dic["observation"+str(i)] = obs.as_dict(ind.Patient_id)
                i = i+1
                #j = j+json.dumps(obs.as_dict(ind.Patient_id), cls=CohortEncoder,  indent=4)

            j = j + json.dumps(person_dic, cls=CohortEncoder, indent=4)

        text_file = open("/Users/babylon/Documents/Covid-19/Data/Cohort.json", "w")
        n = text_file.write(j)
        text_file.close()

    def makeTimeSeries (self):
        column_names = self.getAllColumnNames()
        TimeSeriesDF = pd.DataFrame(columns = column_names)

        for ind in self.individuals:
            observation_list_48hour = getattr(ind, 'observations')

            observation_list_48hour = [x for x in observation_list_48hour if x.Name in column_names]
            observation_list_48hour = [x for x in observation_list_48hour if x.OrdinalTime.days < 4 and x.OrdinalTime.days >= -2]
            observation_list_first_day = [x for x in observation_list_48hour if x.OrdinalTime.days < 1]
            observation_list_second_day = [x for x in observation_list_48hour if (x.OrdinalTime.days < 2 and x.OrdinalTime.days >= 1)]
            observation_list_third_day = [x for x in observation_list_48hour if (x.OrdinalTime.days < 3 and x.OrdinalTime.days >= 2)]

            #get first day observations, mark them into hours 0-23
            for hour in range(0,23):
                hourly_obs_day1 = [x for x in observation_list_first_day if x.OrdinalTime.seconds//3600  == hour]

                hourly_row = [None] * len(column_names)
                hourly_row = dict(zip(column_names, hourly_row))

                for key, value in hourly_row.items():
                    hourly_obs_for_key = [x.Value for x in hourly_obs_day1 if x.Name == key]
                    if len(hourly_obs_for_key)> 0:
                        hourly_row[key] = hourly_obs_for_key[-1]
                    else:
                        hourly_row[key] = np.nan

                hourly_row['PatientID'] = ind.Patient_id
                hourly_row['Hour'] = hour

                if not pd.isnull(ind.DeathDate):
                    hourly_row["Mortality"] = 1
                else:
                    hourly_row["Mortality"] = 0

                if not pd.isnull(ind.ITUDate):
                    hourly_row["ITUAdmission"] = 1
                else:
                    hourly_row["ITUAdmission"] = 0

                AdmitDate = datetime.datetime.strptime(ind.AdmitDate, '%Y-%m-%d')
                SxDate = datetime.datetime.strptime(ind.SxDate, '%Y-%m-%d')
                hourly_row["SxToAdmit"] = AdmitDate - SxDate

                TimeSeriesDF = TimeSeriesDF.append(hourly_row, ignore_index=True)
                print(" df length: ", len(TimeSeriesDF))

           #get second day observations, mark them into hours 24-47
            for hour in range(0,23):
                hourly_obs_day2 = [x for x in observation_list_second_day if x.OrdinalTime.seconds//3600  == hour]

                hourly_row = [None] * len(column_names)
                hourly_row = dict(zip(column_names, hourly_row))

                for key, value in hourly_row.items():
                    hourly_obs_for_key = [x.Value for x in hourly_obs_day2 if x.Name == key]
                    if len(hourly_obs_for_key)> 0:
                        hourly_row[key] = hourly_obs_for_key[-1]
                    else:
                        hourly_row[key] = np.nan

                hourly_row['PatientID'] = ind.Patient_id
                hourly_row['Hour'] = hour+24
                if not pd.isnull(ind.DeathDate):
                    hourly_row["Mortality"] = 1
                else:
                    hourly_row["Mortality"] = 0

                if not pd.isnull(ind.ITUDate):
                    hourly_row["ITUAdmission"] = 1
                else:
                    hourly_row["ITUAdmission"] = 0

                AdmitDate = datetime.datetime.strptime(ind.AdmitDate, '%Y-%m-%d')
                SxDate = datetime.datetime.strptime(ind.SxDate, '%Y-%m-%d')
                hourly_row["SxToAdmit"] = AdmitDate - SxDate

                TimeSeriesDF = TimeSeriesDF.append(hourly_row, ignore_index=True)
                print(" df length: ", len(TimeSeriesDF))

                # get third day observations, mark them into hours 24-47
            for hour in range(0, 23) :
                hourly_obs_day3 = [x for x in observation_list_third_day if x.OrdinalTime.seconds // 3600 == hour]

                hourly_row = [None] * len(column_names)
                hourly_row = dict(zip(column_names, hourly_row))

                for key, value in hourly_row.items() :
                    hourly_obs_for_key = [x.Value for x in hourly_obs_day3 if x.Name == key]
                    if len(hourly_obs_for_key) > 0 :
                        hourly_row[key] = hourly_obs_for_key[-1]
                    else :
                        hourly_row[key] = np.nan

                hourly_row['PatientID'] = ind.Patient_id
                hourly_row['Hour'] = hour + 48
                if not pd.isnull(ind.DeathDate):
                    hourly_row["Mortality"] = 1
                else:
                    hourly_row["Mortality"] = 0

                if not pd.isnull(ind.ITUDate):
                    hourly_row["ITUAdmission"] = 1
                else:
                    hourly_row["ITUAdmission"] = 0

                AdmitDate = datetime.datetime.strptime(ind.AdmitDate, '%Y-%m-%d')
                SxDate = datetime.datetime.strptime(ind.SxDate, '%Y-%m-%d')
                hourly_row["SxToAdmit"] = AdmitDate - SxDate

                TimeSeriesDF = TimeSeriesDF.append(hourly_row, ignore_index=True)
                print(" df length: ", len(TimeSeriesDF))

        na_columns = TimeSeriesDF.columns[2:]

        print("writing time series:")
        TimeSeriesDF = TimeSeriesDF.dropna(how="all", axis=0, subset = na_columns)
        TimeSeriesDF.to_csv("/Users/babylon/Documents/Covid-19/Data/TimeSeries.csv", index=False)
