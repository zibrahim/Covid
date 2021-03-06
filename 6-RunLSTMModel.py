
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from MachineLearning.Models.LSTM.Model import Model
from Processing.Settings import clustered_timeseries_path
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from MachineLearning.MLSetup import scale, stratified_group_k_fold

def plot_results(predicted_data, true_data):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.plot(predicted_data, label='Prediction')
    plt.legend()
    plt.show()


def plot_results_multiple(predicted_data, true_data, prediction_len):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
	# Pad the list of predictions to shift it in the graph to it's correct start
    for i, data in enumerate(predicted_data):
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label='Prediction')
        plt.legend()
    plt.show()

def main():
    configs = json.load(open('MachineLearning/Models/LSTM/Configuration.json', 'r'))
    if not os.path.exists(configs['model']['save_dir']): os.makedirs(configs['model']['save_dir'])

    time_series= pd.read_csv(clustered_timeseries_path+"TimeSeriesAggregatedClusteredDeltaTwoDays.csv")
    print(time_series.shape)
       # configs['data']['train_test_split'],  #the split
        #configs['data']['columns_dynamic'] # the columns

    #Impute and Scale Data


    dynamic_features = configs['data']['dynamic_columns']
    grouping = configs['data']['grouping']
    imp = IterativeImputer(max_iter=10, random_state=0)
    imp.fit(time_series[dynamic_features])
    time_series[dynamic_features] = imp.transform(time_series[dynamic_features])
    time_series = scale(time_series, dynamic_features)

    X = time_series[dynamic_features]
    groups = np.array(time_series[grouping])

    for outcome in configs['data']['classification_outcome']:
        y = time_series[outcome]
        y = y.astype(int)

        model = Model(configs['model']['name'] + outcome)

        print(grouping)
        print(len(set(time_series[grouping])))

        model.build_model(configs)

        i = 0
        for ffold_ind, (training_ind, testing_ind) in enumerate(
                stratified_group_k_fold(X, y, groups, k=10)) :  # CROSS-VALIDATION
            training_groups, testing_groups = groups[training_ind], groups[testing_ind]
            this_y_train, this_y_val = y[training_ind], y[testing_ind]
            this_X_train, this_X_val = X.iloc[training_ind], X.iloc[testing_ind]

            assert len(set(training_groups) & set(testing_groups)) == 0

            print(" X SHAPE: ", this_X_train.shape)
            print(" Y shape: ", this_y_train.shape)


            input_timesteps = 24
            input_dim = 2

            if i == 0:
                #(NumberOfExamples, TimeSteps, FeaturesPerStep).
                model.train(
                    (this_X_train.values).reshape(-1, 24, 35),
                    (this_y_train.values).reshape(-1,24,1))
                i = i +1



if __name__ == '__main__':
    main()