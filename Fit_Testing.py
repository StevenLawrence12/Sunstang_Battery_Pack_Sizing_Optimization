import numpy as np 
import pandas as pd
import glob

path = r'D:\.Steven Data\Extracurricular\Sunstang\2020-2021\Strategy\Code'
filenames = glob.glob(path + "/WSC Energy*.csv")
dfs = [pd.read_csv(f) for f in filenames]
Headers = np.array([['Data Set #', 'Average Velocity (km/h)', 'Average Battery Energy Consumption (kWh)', 'Total Energy Error']])

Genotype_array = np.empty((0, np.size(Headers, axis = 1)))

for x in range(len(filenames)):
    Genotype_array = np.append(Genotype_array, [[x, dfs[x]['Segment Velocity (km/h)'].mean(), dfs[x]['Battery Energy Consumption (kWh)'].mean(), dfs[x]['Energy Difference'].sum()]], axis = 0)

Genotype_df = pd.DataFrame(Genotype_array, columns = Headers[0,:])

Genotype_df.to_csv('Generation Genotypes.csv', index = False)
