import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
import xgboost as xgb
from xgboost import plot_importance, plot_tree
from sklearn.metrics import mean_squared_error, mean_absolute_error

from Processing.Settings import path
plt.style.use('fivethirtyeight')

aggrData = pd.read_csv(path+"TimeSeriesAggregated.csv", index_col=[0], parse_dates=[0])

plot_data = aggrData[['PatientID','PO2/FIO2']]
color_pal = ["#F8766D", "#D39200", "#93AA00", "#00BA38", "#00C19F", "#00B9E3", "#619CFF", "#DB72FB"]
_ = aggrData.plot(style='.', figsize=(15,5), color=color_pal[0], title='PJM East')