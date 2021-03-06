from Cohort.Cohort import Cohort
from Cohort.Patient import Patient
from Cohort.Observation import Observation
from Processing.Utils import getDayWrapper, getHourWrapper
from Processing.Settings import data_path
import json
import numpy as np
from datetime import datetime, timedelta
import pandas as pd

class CohortEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, timedelta):
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
            observation_df = observation_df.loc[observation_df.Day <= 1]

            days = pd.Series([-1,0,1])

            PatientDF['Day'] = days.repeat(24)

            PatientDF.loc[PatientDF.Day == -1, "Hour"] = range(-24,0)
            PatientDF.loc[PatientDF.Day == 0, "Hour"] = range(0,24)
            PatientDF.loc[PatientDF.Day == 1, "Hour"] = range(24,48)

            PatientDF.loc[PatientDF.Day == -1, "OrdinalHour"] = range(0,24)
            PatientDF.loc[PatientDF.Day == 0, "OrdinalHour"] = range(0,24)
            PatientDF.loc[PatientDF.Day == 1, "OrdinalHour"] = range(0,24)

            PatientDF['PatientID'] = ind.Patient_id
            PatientDF['Age'] = ind.Age

            PatientDF["Mortality"] = 1 if not pd.isnull(ind.DeathDate)  else 0
            PatientDF["NumComorbidities"] = ind.Asthma + ind.CKD + ind.COPD + ind.HF + ind.IHD + ind.HTN + ind.Diabetes

            PatientDF["ITUAdmission"] = 1 if not pd.isnull(ind.ITUDate)  else 0
            AdmitDate = datetime.strptime(ind.AdmitDate, '%Y-%m-%d')
            SxDate = datetime.strptime(ind.SxDate, '%Y-%m-%d')

            ITURange = 8000

            if (not pd.isnull(ind.ITUDate)) :
                ITUDate = datetime.strptime(ind.ITUDate, '%Y-%m-%d')
                ITURange = ITUDate  - AdmitDate

            if ((not (pd.isnull(ind.ITUDate))) and (ITURange <= timedelta(days=3))) :
                PatientDF['ITUAdmission3Days'] = 1
            else:
                PatientDF['ITUAdmission3Days'] = 0

            if ((not (pd.isnull(ind.ITUDate))) and (ITURange <= timedelta(days=5))) :
                PatientDF['ITUAdmission5Days'] = 1
            else:
                PatientDF['ITUAdmission5Days'] = 0


            if ((not (pd.isnull(ind.ITUDate))) and (ITURange <= timedelta(days=7))) :
                PatientDF['ITUAdmission7Days'] = 1
            else:
                PatientDF['ITUAdmission7Days'] = 0

            if ((not (pd.isnull(ind.ITUDate))) and (ITURange <= timedelta(days=14))) :
                PatientDF['ITUAdmission14Days'] = 1
            else:
                PatientDF['ITUAdmission14Days'] = 0

            if ((not (pd.isnull(ind.ITUDate))) and (ITURange <= timedelta(days=30))) :
                PatientDF['ITUAdmission30Days'] = 1
            else :
                PatientDF['ITUAdmission30Days'] = 0

            deathRange = 8000

            if (not pd.isnull(ind.DeathDate)):
                DeathDate = datetime.strptime(ind.DeathDate, '%Y-%m-%d')
                deathRange = DeathDate - AdmitDate

            if ((not (pd.isnull(ind.DeathDate))) and (deathRange <= timedelta(days=3))) :
                PatientDF['Mortality3Days'] = 1
            else:
                PatientDF['Mortality3Days'] = 0

            if ((not (pd.isnull(ind.DeathDate))) and (deathRange <= timedelta(days=5))) :
                PatientDF['Mortality5Days'] = 1
            else :
                PatientDF['Mortality5Days'] = 0

            if ((not (pd.isnull(ind.DeathDate))) and (deathRange <= timedelta(days=7))) :
                PatientDF['Mortality7Days'] = 1
            else:
                PatientDF['Mortality7Days'] = 0

            if ((not (pd.isnull(ind.DeathDate))) and (deathRange <= timedelta(days=14))) :
                PatientDF['Mortality14Days'] = 1
            else:
                PatientDF['Mortality14Days'] = 0

            if ((not (pd.isnull(ind.DeathDate))) and (deathRange <= timedelta(days=30))) :
                PatientDF['Mortality30Days'] = 1
            else:
                PatientDF['Mortality30Days'] = 0

            PatientDF["SxToAdmit"] = AdmitDate - SxDate

            for index, row in observation_df.iterrows() :
                ob_name = row['ObservationName']
                ob_value = row['ObservationValue']
                ob_hour = row['Hour']
                ob_day = row['Day']

                PatientDF.loc[(PatientDF.Day == ob_day) & (PatientDF.OrdinalHour == ob_hour), ob_name] = ob_value
            TimeSeriesDF = TimeSeriesDF.append((PatientDF))
        TimeSeriesDF.to_csv(data_path+"TimeSeries.csv", index=False)
        observation_df.to_csv(data_path+"obs.csv", index=False)