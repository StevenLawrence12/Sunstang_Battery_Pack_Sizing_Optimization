import numpy as np
import pandas as pd 

dfs = pd.read_csv('Generation Genotypes.csv')
#print(dfs)

num_parents = 4
parents = np.empty((num_parents, dfs['Data Set #'].shape[0]))

for parent_num in range(num_parents):

    max_fitness_idx = np.where(dfs['ASC Score'] == np.max(dfs['ASC Score']))

    max_fitness_idx = max_fitness_idx[0][0]
    print(max_fitness_idx)

    #parents[parent_num, :] = dfs[max_fitness_idx, :]

    dfs['ASC Score'][max_fitness_idx] = -99999999999

