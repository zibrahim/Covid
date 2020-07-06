import pandas as pd
import numpy as np

def clean_vitals(vitals):
    column_names = ['DateTime', 'Temperature', 'OxygenSaturation', 'RespirationRate', 'SupplementalOxygen',
                    'OxygenDelivery', 'OxygenLitres', 'HeartRate', 'SysBP', 'DiasBP', 'PainScore', 'GCSEye',
                    'GCSVerbal', 'GCSMotor', 'NEWS2', 'DateTimeRaw', 'Patient_ID']
    vitals.columns = column_names
    vitals.DateTime = updateDateTime(vitals.DateTime)
    vitals["SupplementalOxygen"] = vitals["SupplementalOxygen"].astype('category')
    vitals["SupplementalOxygen"] = vitals["SupplementalOxygen"].cat.codes  # No (Air) = 0, Yes = 1

    vitals["OxygenDelivery"] = vitals["OxygenDelivery"].astype('category')
    vitals["OxygenDelivery"] = vitals["OxygenDelivery"].cat.codes  # No (Air) = 0, Yes = 1

    #These values: array([nan, 'Nasal Cannula', 'Venturi Mask', 'Nebuliser',
       #'Humidified System', 'Non-rebreather mask', 'CPAP', 'Simple Mask',
       #'ET', 'Optiflow', 'Trachy', 'BIPAP', 'I-Gel'], dtype=object)

    # Map to these values: array([-1,  5, 11,  6,  3,  7,  1,  9,  2,  8, 10,  0,  4])
    return vitals

def clean_blood(bloods):

    #### ZI: merge PH and PH(T) and check: 'pH on 1l with Ahmed
    bloods.loc[bloods.basicobs_itemname_analysed == '.pH', 'basicobs_itemname_analysed'] = 'PH'
    bloods.loc[bloods.basicobs_itemname_analysed == 'pH(T)', 'basicobs_itemname_analysed'] = 'PH'
    bloods.loc[bloods.basicobs_itemname_analysed == 'Blood pH', 'basicobs_itemname_analysed'] = 'PH'

    bloods.loc[bloods.basicobs_itemname_analysed == 'CSF Glucose.', 'basicobs_itemname_analysed'] = 'CSF Glucose'

    bloods.loc[bloods.basicobs_itemname_analysed == 'Bicarbonate:', 'basicobs_itemname_analysed'] = 'Bicarbonate'
    bloods.loc[bloods.basicobs_itemname_analysed == 'Bicarbonate.', 'basicobs_itemname_analysed'] = 'Bicarbonate'
    bloods.loc[bloods.basicobs_itemname_analysed == 'Blood Lactate.', 'basicobs_itemname_analysed'] = 'Blood Lactate'

    bloods.loc[bloods.basicobs_itemname_analysed == '.pCO2', 'basicobs_itemname_analysed'] = 'PCO2'
    bloods.loc[bloods.basicobs_itemname_analysed == 'pCO2(T)', 'basicobs_itemname_analysed'] = 'PCO2'

    bloods.loc[bloods.basicobs_itemname_analysed == 'HBA1c (IFCC)', 'basicobs_itemname_analysed'] = 'HBA1c-IFCC'
    bloods.loc[bloods.basicobs_itemname_analysed == 'HBA1c (IFCC).', 'basicobs_itemname_analysed'] = 'HBA1c-IFCC'
    bloods.loc[bloods.basicobs_itemname_analysed == 'HbA1c IFCC', 'basicobs_itemname_analysed'] = 'HBA1c-IFCC'

    bloods.loc[bloods.basicobs_itemname_analysed == 'HbA1c (DCCT)', 'basicobs_itemname_analysed'] = 'HBA1c-DCCT'
    bloods.loc[bloods.basicobs_itemname_analysed == 'HbA1c (DCCT).', 'basicobs_itemname_analysed'] = 'HBA1c-DCCT'
    bloods.loc[bloods.basicobs_itemname_analysed == 'HBA1c (DCCT).', 'basicobs_itemname_analysed'] = 'HBA1c-DCCT'
    bloods.loc[bloods.basicobs_itemname_analysed == 'HBA1c (DCCT)', 'basicobs_itemname_analysed'] = 'HBA1c-DCCT'
    bloods.loc[bloods.basicobs_itemname_analysed == 'HBA1c DCCT', 'basicobs_itemname_analysed'] = 'HBA1c-DCCT'
    bloods.loc[bloods.basicobs_itemname_analysed == 'HbA1c DCCT', 'basicobs_itemname_analysed'] = 'HBA1c-DCCT'

    bloods.loc[bloods.basicobs_itemname_analysed == 'Lymphocytes.', 'basicobs_itemname_analysed'] = 'Lymphocytes'


    bloods.loc[bloods.basicobs_itemname_analysed == '.pO2', 'basicobs_itemname_analysed'] = 'PO2'
    bloods.loc[bloods.basicobs_itemname_analysed == 'pO2(T)', 'basicobs_itemname_analysed'] = 'PO2'

    bloods.loc[bloods.basicobs_itemname_analysed == 'pO2(a,T)/FIO2', 'basicobs_itemname_analysed'] = 'PO2/FIO2'
    bloods.loc[bloods.basicobs_itemname_analysed == 'pO2(a)/FIO2', 'basicobs_itemname_analysed'] = 'PO2/FIO2'

    bloods.loc[bloods.basicobs_itemname_analysed == 'INR.', 'basicobs_itemname_analysed'] = 'INR'

    bloods.loc[bloods.basicobs_itemname_analysed == 'WBC.', 'basicobs_itemname_analysed'] = 'WBC'

    bloods.loc[bloods.basicobs_itemname_analysed == 'Random Urine Creatinine.', 'basicobs_itemname_analysed'] = 'Random-Urine-Creatinine'
    bloods.loc[bloods.basicobs_itemname_analysed == 'Random Urine Creatinine', 'basicobs_itemname_analysed'] = 'Random-Urine-Creatinine'
    bloods.loc[bloods.basicobs_itemname_analysed == 'Urine Creatinine(Random)', 'basicobs_itemname_analysed'] = 'Random-Urine-Creatinine'
    bloods.loc[bloods.basicobs_itemname_analysed == 'Urine Creatinine (Random)', 'basicobs_itemname_analysed'] = 'Random-Urine-Creatinine'
    bloods.loc[bloods.basicobs_itemname_analysed == 'Urine Creatinine.', 'basicobs_itemname_analysed'] = 'Random-Urine-Creatinine'



    bloods.loc[bloods.basicobs_itemname_analysed == "Hb.", 'basicobs_itemname_analysed'] = "Hb"
    bloods.loc[bloods.basicobs_itemname_analysed == 'Troponin T..', 'basicobs_itemname_analysed'] = 'Troponin-T'
    bloods.loc[bloods.basicobs_itemname_analysed == 'Troponin T.', 'basicobs_itemname_analysed'] = 'Troponin-T'
    bloods.loc[bloods.basicobs_itemname_analysed == 'Troponin T', 'basicobs_itemname_analysed'] = 'Troponin-T'
    bloods.loc[bloods.basicobs_itemname_analysed == 'Troponin I', 'basicobs_itemname_analysed'] = 'Troponin-I'
    bloods.loc[bloods.basicobs_itemname_analysed == 'Troponin I.', 'basicobs_itemname_analysed'] = 'Troponin-I'


    bloods.loc[
        bloods.basicobs_itemname_analysed == 'Neutrophils (manual diff)', 'basicobs_itemname_analysed'] = 'Neutrophils'
    bloods.loc[bloods.basicobs_itemname_analysed == 'NT-proBNP', 'basicobs_itemname_analysed'] = 'NT-pro-BNP'
    bloods.loc[bloods.basicobs_itemname_analysed == "Ferritin'", 'basicobs_itemname_analysed'] = 'Ferritin'
    bloods.loc[
        bloods.basicobs_itemname_analysed == 'Lactate Dehydrogenase.', 'basicobs_itemname_analysed'] = 'Lactate-Dehydrogenase'
    bloods.loc[
        bloods.basicobs_itemname_analysed == 'Lactate Dehydrogenase', 'basicobs_itemname_analysed'] = 'Lactate-Dehydrogenase'
    bloods.loc[bloods.basicobs_itemname_analysed == 'CRP.', 'basicobs_itemname_analysed'] = 'C-Reactive-Protein'
    bloods.loc[bloods.basicobs_itemname_analysed == 'CRP', 'basicobs_itemname_analysed'] = 'C-Reactive-Protein'
    bloods.loc[
        bloods.basicobs_itemname_analysed == 'C-reactive Protein', 'basicobs_itemname_analysed'] = 'C-Reactive-Protein'
    bloods.loc[bloods.basicobs_itemname_analysed == 'Lactate.', 'basicobs_itemname_analysed'] = 'Lactate'
    bloods.loc[bloods.basicobs_itemname_analysed == 'Creatine Kinase', 'basicobs_itemname_analysed'] = 'Creatine-Kinase'

    bloods.loc[
        bloods.basicobs_itemname_analysed == 'Aspartate Transaminase', 'basicobs_itemname_analysed'] = 'Aspartate-Transaminase'
    bloods.loc[bloods.basicobs_itemname_analysed == 'Estimated GFR', 'basicobs_itemname_analysed'] = 'Estimated-GFR'
    bloods.loc[bloods.basicobs_itemname_analysed == 'HbA1c %', 'basicobs_itemname_analysed'] = 'HbA1c'

    bloods.updatetime = removeDateSuffix(bloods["updatetime"])
    bloods.updatetime = updateDateTime(bloods.updatetime)
    return bloods


def clean_outcomes(outcomes):
    outcomes.Ethnicity.unique()
    outcomes_cleaned = pd.DataFrame()
    outcomes_cleaned["PatientID"] = outcomes.patient_pseudo_id
    outcomes_cleaned["Age"] = outcomes.Age

    outcomes_cleaned["Gender"] = outcomes["Male"].astype('category')
    outcomes_cleaned["Gender"] = outcomes_cleaned["Gender"].cat.codes  # Female = 0, Male = 1

    outcomes_cleaned["SxDate"] = outcomes["Sx Date"]
    outcomes_cleaned["SxDate"] = updateDate(outcomes_cleaned["SxDate"])

    outcomes_cleaned["AdmitDate"] = outcomes["Admit Date"]
    outcomes_cleaned["AdmitDate"] = updateDate(outcomes_cleaned["AdmitDate"])

    outcomes_cleaned["DeathDate"] = outcomes["Death Date"]
    outcomes_cleaned["DeathDate"] = updateDate(outcomes_cleaned["DeathDate"])

    outcomes_cleaned["ITUDate"] = outcomes["ITU date"]
    outcomes_cleaned["ITUDate"] = updateDate(outcomes_cleaned["ITUDate"])

    outcomes_cleaned["Ethnicity"] = outcomes["Ethnicity"].astype('category')
    outcomes_cleaned["Ethnicity"] = outcomes_cleaned[
        "Ethnicity"].cat.codes  # Unknown: 3, Caucasian: 2, Black 1, Asian: 0

    outcomes_cleaned["COPD"] = outcomes["COPD"].astype('category')
    outcomes_cleaned["COPD"] = outcomes_cleaned["COPD"].cat.codes

    outcomes_cleaned["Asthma"] = outcomes["Asthma"].astype('category')
    outcomes_cleaned["Asthma"] = outcomes_cleaned["Asthma"].cat.codes

    outcomes_cleaned["HF"] = outcomes["HF"].astype('category')
    outcomes_cleaned["HF"] = outcomes_cleaned["HF"].cat.codes

    outcomes_cleaned["Diabetes"] = outcomes["Diabetes"].astype('category')
    outcomes_cleaned["Diabetes"] = outcomes_cleaned["Diabetes"].cat.codes

    outcomes_cleaned["IHD"] = outcomes["IHD"].astype('category')
    outcomes_cleaned["IHD"] = outcomes_cleaned["IHD"].cat.codes

    outcomes_cleaned["HTN"] = outcomes["HTN"].astype('category')
    outcomes_cleaned["HTN"] = outcomes_cleaned["HTN"].cat.codes

    outcomes_cleaned["CKD"] = outcomes["CKD"].astype('category')
    outcomes_cleaned["CKD"] = outcomes_cleaned["CKD"].cat.codes
    return outcomes_cleaned


def removeDateSuffix(df):
    dates = []
    for s in df:
        parts = s.split()
        parts[1] = parts[1].strip("stndrh") # remove 'st', 'nd', 'rd', ...
        dates.append(" ".join(parts))

    return dates

def updateDate(df):
    date_output_format = "%Y-%m-%d"

    dates = []
    for t in df:
        if t == '' or pd.isnull(t) :
            d = np.nan
        elif "-" in t :
            fmt = "%y-%m-%d"
            d = pd.to_datetime(t, format=fmt, exact=False, utc=True)
        elif "/" in t :
            fmt = "%d/%m/%y"
            d = pd.to_datetime(t, format=fmt, exact=False)
        else :
            fmt = None
            d = pd.to_datetime(t, format=fmt, exact=False)
        if pd.isnull(d):
            dates.append(np.nan)
        else:
            dates.append(d.strftime(date_output_format))
    return dates

def updateDateTime(df):
    date_output_format = "%Y-%m-%d %H:%M:%S"
    dates = []
    for t in df:
        if "-" in t :
            fmt = "%y-%m-%d %H:%M"
            d = pd.to_datetime(t, format=fmt, exact=False, utc=True)
        elif "/" in t :
            fmt = "%d/%m/%y %H:%M"
            d = pd.to_datetime(t, format=fmt, exact=False)
        else :
            fmt = None
            d = pd.to_datetime(t, format=fmt, exact=False)
        dates.append(d.strftime(date_output_format))
    return dates
