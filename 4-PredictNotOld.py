import pandas as pd
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn import metrics
import matplotlib.pyplot as plt
import shap as sp
import lime as lm
from tqdm import tqdm


from Processing.Settings import path

def InputData():
    dataset=pd.read_csv(path+"TimeSeriesAggregated.csv")
    """
    print('Datasize: %d x %d'%(len(dataset.index),len(dataset.columns)))
    count=0
    for i in range(2,len(dataset.columns)):
        for j in range(0,len(dataset.index)):
            if pd.isna(dataset[dataset.columns[i]][j]):
                if count is 0:
                    print(dataset.columns[i],end=': ')
                count+=1
        if count is not 0:
            print(count)
            count=0
    """
    try:
        with tqdm(range(2,len(dataset.columns))) as bar:
            ftName=[]
            for i in bar:
                dataset[dataset.columns[i]]=dataset[dataset.columns[i]].fillna(dataset[dataset.columns[i]].mean())
                ftName.append(dataset.columns[i])
    except KeyboardInterrupt:
        bar.close()
        raise
    bar.close()
    x=dataset[ftName]
    y=dataset[dataset.columns[1]]
    return x,y

def main():
    time_series = pd.read_csv(path+"TimeSeriesAggregated.csv")

    pd.options.mode.chained_assignment = None
    x, y = InputData()

    print(x.columns)
    print(y.head())
    xgbm=xgb.XGBClassifier(scale_pos_weight=263/73,
                           learning_rate=0.007,
                           n_estimators=100,
                           gamma=0,
                           max_depth=4,
                           min_child_weight=2,
                           subsample=1,
                           eval_metric='error')
    rfm=RandomForestClassifier(n_estimators=100,
                               max_depth=4)
    lrm=LogisticRegression(solver='lbfgs')


    #ExperimentI(x,y,xgbm,rfm,lrm)
    #ExperimentII(x,y,xgbm,rfm,lrm)
    #ExperimentIII(x,y,rfm,lrm)
    #ExperimentIV(x,y,xgbm,rfm,lrm)
    #ExperimentV(x,y,xgbm,rfm,lrm)
    #ExperimentVI(x,y,xgbm,rfm,lrm)
    #ExperimentVII(xgbm,rfm,lrm)
    #ExperimentVIII(x,y,xgbm,rfm,lrm)

if __name__ == '__main__':
    main()
