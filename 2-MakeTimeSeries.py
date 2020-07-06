from Processing.Serialisation import jsonRead, makeTimeSeries
from Processing.Settings import path
def main():
    cohort = jsonRead(path+"Cohort.json")
    makeTimeSeries(cohort)

if __name__ == "__main__":
    main()