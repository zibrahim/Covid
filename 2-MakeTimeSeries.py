from Processing.Serialisation import jsonRead, makeTimeSeries
from Processing.Settings import data_path
def main():
    cohort = jsonRead(data_path+"Cohort.json")
    makeTimeSeries(cohort)

if __name__ == "__main__":
    main()