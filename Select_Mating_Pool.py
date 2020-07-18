import numpy as np
import pandas as pd 

GG_df = pd.read_csv('Generation Genotypes.csv')
#print(dfs)

num_parents = 4
parents_vel_df = []

for parent_num in range(num_parents):

    max_fitness_idx = np.where(GG_df['ASC Score'] == np.max(GG_df['ASC Score']))

    max_fitness_idx = max_fitness_idx[0][0]
    print(max_fitness_idx)
    parents_vel_df.append(pd.read_csv(f'WSC Energy Management Model({max_fitness_idx}).csv', usecols = ['Segment Velocity (km/h)']))
    
    GG_df['ASC Score'][max_fitness_idx] = -99999999999


parents = pd.concat(parents_vel_df, axis = 1, ignore_index = True)
print(parents)

parents.to_csv('Breeding_Parents.csv', index = False, header = False)

