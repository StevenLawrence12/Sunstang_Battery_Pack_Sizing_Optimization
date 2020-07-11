import numpy as np
import pandas as pd 
import glob

path = r'D:\.Steven Data\Extracurricular\Sunstang\2020-2021\Strategy\Code'
filenames = glob.glob(path + "/WSC Energy*.csv")
dfs = [pd.read_csv(f) for f in filenames]

a = np.array([['Data Set #', 'Average Velocity (km/h)', 'Average Battery Energy Consumption (kWh)', 'Total Energy Error']])
for x in range(len(filenames)):
    a = np.append(a, [[x, dfs[x]['Segment Velocity (km/h)'].mean(), dfs[x]['Battery Energy Consumption (kWh)'].mean(), dfs[x]['Energy Difference'].sum()]], axis = 0)
