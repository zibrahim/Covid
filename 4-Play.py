import pandas as pd
import xgboost as xgb

from Processing.Settings import path

def main():
    time_series = pd.read_csv(path+"TimeSeriesAggregated.csv")

    xgbm=xgb.XGBClassifier(scale_pos_weight=263/73,
                           learning_rate=0.007,
                           n_estimators=100,
                           gamma=0,
                           max_depth=4,
                           min_child_weight=2,
                           subsample=1,
                           eval_metric='error')


if __name__ == '__main__':
    main()
