from Cohort.Cohort import Cohort
from Cohort.Patient import Patient
from Cohort.Observation import Observation
from Processing.Helpers import getDayWrapper, getHourWrapper
from Processing.Settings import path
import json
import numpy as np
import datetime
import pandas as pd

class CohortEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, datetime.timedelta):
            return str(obj)
        else:
            return super(CohortEncoder, self).default(obj)

def jsonDump ( cohort, filename ) :
        json_dict = {}
        individuals = []
        for ind in cohort.individuals :
            person_dic = ind.as_dict()
            i = 0
            observations = []
            for obs in ind.__getattribute__("observations") :
                observations.append(obs.as_dict(ind.Patient_id))
                i = i + 1
            person_dic["observations"] = observations
            individuals.append(person_dic)

        json_dict["cohort"] = cohort.name
        json_dict["patients"] = individuals

        with open(filename, "w") as outfile :
            json.dump(json_dict, outfile, cls=CohortEncoder,indent=4, sort_keys=True)


def jsonRead(fileName):

    with open(fileName) as f :
        cohort_dict = json.load(f)
        patients = cohort_dict['patients']
        cohort = Cohort(cohort_dict['cohort'])

        for p in patients:
            patient = Patient(p['PatientID'], p['Age'], p['Gender'], p['SxDate'], p['AdmitDate'], p['DeathDate'],
                                p['ITUDate'],p['Ethnicity'], p['COPD'], p['Asthma'],
                                p['HF'], p['Diabetes'], p['IHD'], p['HTN'], p['CKD'])

            observations_dictionary = p['observations']
            observations = []
            for o in observations_dictionary:
                new_obs =  Observation(o['ObservationType'],
                                       o['ObservationName'],
                                       o['ObservationOrdinalTime'],
                                       o['ObservationValue'],
                                       o['ObservationUnit'],
                                       o['ObservationText'])

                observations.append(new_obs)

            patient.addObservations(observations)
            cohort.addIndividual(patient, p['PatientID'])

    return cohort

def makeTimeSeries( cohort ):
        column_names = cohort.getAllColumnNames()
        TimeSeriesDF = pd.DataFrame(columns= column_names)
        PatientDF = pd.DataFrame(columns = column_names)
        cohort.clean()
        print(len(cohort.individual_ids))
        for ind in cohort.individuals:
            observation_list = getattr(ind, 'observations')

            observation_list = [x for x in observation_list if x.Name in column_names]

            observation_df = pd.DataFrame.from_records([o.as_dict(ind.Patient_id) for o in observation_list])
            observation_df['Day'] = observation_df.apply(lambda x: getDayWrapper(x['ObservationOrdinalTime']),axis=1)
            observation_df['Hour'] = observation_df.apply(lambda x: getHourWrapper(x['ObservationOrdinalTime']),axis=1)


            observation_df['Day'] = observation_df['Day'].astype(int)
            observation_df['Hour'] = observation_df['Hour'].astype(int)


            #Subset observations to include days -1 to 2
            observation_df = observation_df.loc[observation_df.Day >=-1]
            observation_df = observation_df.loc[observation_df.Day <= 2]

            days = pd.Series([-1,0,1,2])

            PatientDF['Day'] = days.repeat(24)

            PatientDF.loc[PatientDF.Day == -1, "Hour"] = range(-24,0)
            PatientDF.loc[PatientDF.Day == 0, "Hour"] = range(0,24)
            PatientDF.loc[PatientDF.Day == 1, "Hour"] = range(24,48)
            PatientDF.loc[PatientDF.Day == 2, "Hour"] = range(48,72)

            PatientDF.loc[PatientDF.Day == -1, "OrdinalHour"] = range(0,24)
            PatientDF.loc[PatientDF.Day == 0, "OrdinalHour"] = range(0,24)
            PatientDF.loc[PatientDF.Day == 1, "OrdinalHour"] = range(0,24)
            PatientDF.loc[PatientDF.Day == 2, "OrdinalHour"] = range(0,24)

            PatientDF['PatientID'] = ind.Patient_id
            PatientDF["Mortality"] = 1 if not pd.isnull(ind.DeathDate)  else 0
            PatientDF["ITUAdmission"] = 1 if not pd.isnull(ind.ITUDate)  else 0
            AdmitDate = datetime.datetime.strptime(ind.AdmitDate, '%Y-%m-%d')
            SxDate = datetime.datetime.strptime(ind.SxDate, '%Y-%m-%d')
            PatientDF["SxToAdmit"] = AdmitDate - SxDate

            for index, row in observation_df.iterrows() :
                ob_name = row['ObservationName']
                ob_value = row['ObservationValue']
                ob_time = row['ObservationOrdinalTime']
                ob_hour = row['Hour']
                ob_day = row['Day']

                PatientDF.loc[(PatientDF.Day == ob_day) & (PatientDF.OrdinalHour == ob_hour), ob_name] = ob_value
            TimeSeriesDF = TimeSeriesDF.append((PatientDF))
        TimeSeriesDF.to_csv(path+"TimeSeries.csv", index=False)
        observation_df.to_csv(path+"obs.csv", index=False)
