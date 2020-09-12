import numpy as np
import pandas as pd 

def Mating_Main(Output, GG_df, Data_Frames, Counter):

    num_parents = 4
    parents_vel_df = []

    for parent_num in range(num_parents):

        max_fitness_idx = np.where(GG_df['ASC Score'] == np.max(GG_df['ASC Score']))

        max_fitness_idx = max_fitness_idx[0][0]
        parents_vel_df.append(Data_Frames[max_fitness_idx]['Segment Velocity (km/h)'])

        GG_df['ASC Score'][max_fitness_idx] = -99999999999


    parents = pd.concat(parents_vel_df, axis = 1, ignore_index = True)

    if Counter == 99:
        parents.to_csv(Output + '\Breeding_Parents.csv', index = False, header = False)

    return parents
