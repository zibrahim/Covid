import pandas as pd
import traceback
from keras.models import Model
from keras.layers import Dense, LSTM, Input, Masking
from MachineLearning.MLSetup import lstm_precision, lstm_recall, lstm_matthews,\
    lstm_dict, stratified_group_k_fold,lstm_running_params, generate_balanced_arrays
from Processing.Settings import lstm_stats_path

from keras.activations import sigmoid

from sklearn.metrics import roc_auc_score, matthews_corrcoef
from keras.callbacks import ModelCheckpoint, EarlyStopping

#SUPPLY LSTM WITH THE TRAINING X AND Y! SUPPLY WITH ALL_ARGS IN THE ORIGINAL SCRIPT


def create_model(X,y, outcome, groups, experiment_number):
    AUCheader = ['auc_train', 'auc_val', 'matthews_train', 'matthews_val', 'cv_num'] + list(lstm_dict.keys())
    CVheader = ['acc', 'loss', 'matthews', 'precision', 'recall', 'val_acc', 'val_loss', 'val_matthews',
                'val_precision', 'val_recall', 'cv_num'] + list(lstm_dict.keys())
    errorHeader = ['error', 'args']
    activation = lstm_dict['activation'][0]
    batch = lstm_dict['batch'][0]
    data = lstm_dict['data'][0]
    dropout = lstm_dict['dropout'][0]
    layers = lstm_dict['layers'][0]
    masking = lstm_dict['masking'][0]
    optimizer = lstm_dict['optimizer'][0]
    units = lstm_dict['units'][0]


    n_hidden = 1
    input_layer = Input(shape=(X.shape[0], X.shape[1]))
    if masking :
      # masking layer
        masking_layer = Masking(mask_value=0.)(input_layer)
        if layers == 1 :# add first LSTM layer
            lstm = LSTM(units, activation=sigmoid, recurrent_dropout=dropout)(masking_layer)
        else :# add first LSTM layer
            lstm = LSTM(units, activation=sigmoid, recurrent_dropout=dropout,
             return_sequences=True)(masking_layer)
    else :
        if layers == 1 :# add first LSTM layer
            lstm = LSTM(units, activation=sigmoid, recurrent_dropout=dropout)(input_layer)
        else :
            lstm = LSTM(units, activation=sigmoid, recurrent_dropout=dropout,return_sequences=True)(input_layer)
    while n_hidden < layers :
        n_hidden += 1
        if n_hidden == layers :# add additional hidden layers
            lstm = LSTM(units, activation=sigmoid, recurrent_dropout=dropout)(lstm)
        else :
            lstm = LSTM(units, activation=activation, recurrent_dropout=dropout, return_sequences=True)(lstm)

 # add output layer
    output_layer = Dense(1, activation=sigmoid)(lstm)
    model = Model(inputs=input_layer, outputs=output_layer)
    model.compile(loss='binary_crossentropy', optimizer=optimizer,metrics=['accuracy', lstm_precision, lstm_recall,
                                                                         lstm_matthews])
    initial_weights_path = lstm_stats_path + "/best_weights/" + '_'.join(['initial_weights', 'sigmoid', str(batch),
                                                                   data, str(dropout),str(layers), str(masking),
                                                                   optimizer, outcome, str(units)])+ '.hdf5'
    model.save_weights(initial_weights_path)
    i = 0


    for fold_ind, (training_ind, testing_ind) in enumerate(
          stratified_group_k_fold(X, y, groups, k=10)) :  # CROSS-VALIDATION
      training_groups, testing_groups = groups[training_ind], groups[testing_ind]
      this_y_train, this_y_val = y[training_ind], y[testing_ind]
      this_X_train, this_X_val = X.iloc[training_ind], X.iloc[testing_ind]

      # print("Training X", training_X['ALT'], "Training y", training_y)
      # print(type(training_groups), type(testing_groups))
      assert len(set(training_groups) & set(testing_groups)) == 0

      if batch == 'all':
        batch_size = this_X_train.shape[0]
      else:
        batch_size = batch

      filepath = lstm_stats_path + "/best_weights/" + '_'.join([activation, str(batch),
                                                       data, str(dropout), str(layers),
                                                       str(masking), optimizer, outcome,
                                                       str(units), str(i)]) + '.hdf5'

      checkpoint = ModelCheckpoint(filepath, monitor=lstm_running_params['monitor_checkpoint'][0],
                                   verbose=0, save_best_only=True,
                                   mode=lstm_running_params['monitor_checkpoint'][1])

      # define early stopping
      earlystopping = EarlyStopping(monitor=lstm_running_params['monitor_early_stopping'][0],
                                    min_delta=0, patience=lstm_running_params['patience'],
                                    verbose=0, mode=lstm_running_params['monitor_early_stopping'][1])

      # define callbacks_list
      callbacks_list = []
      if lstm_running_params['early_stopping'] :
          callbacks_list.append(earlystopping)
      if lstm_running_params['save_checkpoint']:
          callbacks_list.append(checkpoint)
      # TRAIN MODEL
      if data == "balanced":
        train_hist = model.fit_generator(generate_balanced_arrays(this_X_train, this_y_train),
                                       callbacks=callbacks_list,
                                       epochs=lstm_running_params['n_epochs'],
                                       validation_data=[this_X_val, this_y_val],
                                       steps_per_epoch=1,
                                       verbose=0)

      elif data == "unchanged":
            train_hist = model.fit(this_X_train, this_y_train,
                             callbacks=callbacks_list,
                             epochs=lstm_running_params['n_epochs'],
                             validation_data=[this_X_val, this_y_val],
                             batch_size=batch_size,
                             verbose=0)

      try :# reload best weights
        model.load_weights(filepath)

        # calculate model prediction classes
        y_pred_train = model.predict(this_X_train)
        y_pred_val = model.predict(this_X_val)

        y_pred_train_binary = (y_pred_train > 0.5).astype('int32')
        y_pred_val_binary = (y_pred_val > 0.5).astype('int32')

        # append AUC score to existing file
        AUChistory = pd.DataFrame(columns=AUCheader)

        AUChistory = AUChistory.append({'auc_train' : roc_auc_score(this_y_train, y_pred_train),
                                      'auc_val' : roc_auc_score(this_y_val, y_pred_val),
                                      'matthews_train' : matthews_corrcoef(this_y_train,
                                                                           y_pred_train_binary),
                                      'matthews_val' : matthews_corrcoef(this_y_val,
                                                                         y_pred_val_binary),
                                      'data' : data,
                                      'cv_num' : i,
                                      'activation' : activation,
                                      'dropout' : dropout,
                                      'units' : units,
                                      'optimizer' : optimizer,
                                      'batch' : batch,
                                      'layers' : layers,
                                      'masking' : masking,
                                      'outcome' : outcome}, ignore_index=True)
        AUChistory.to_csv('Experiment'+experiment_number+'AUC_history_gridsearch'+outcome+'.tsv', header=None, index=False,
                        sep='\t', mode='a', columns=AUCheader)

        # append other scores to existing file
        model_history = pd.DataFrame.from_dict(train_hist.history)
        model_history['data'] = data
        model_history['cv_num'] = i
        model_history['activation'] = activation
        model_history['dropout'] = dropout
        model_history['units'] = units
        model_history['optimizer'] = optimizer
        model_history['batch'] = batch
        model_history['layers'] = layers

        model_history['masking'] = masking
        model_history['outcome'] = outcome

        model_history.to_csv('Experiment'+experiment_number+'CV_history_gridsearch'+outcome+'.tsv', header=None, index=True,
                           sep='\t', mode='a', columns=CVheader)

      except:
        var = traceback.format_exc()
        args = activation + batch + data + dropout + layers + masking + optimizer + outcome
        errorDF = pd.DataFrame(columns=errorHeader)
        errorDF = errorDF.append({'error' : var,
                                'args' : args}, ignore_index=True)
        errorDF.to_csv('Experiment'+experiment_number+'error.log', header=None, index=False,
                     sep='\t', mode='a', columns=errorHeader)