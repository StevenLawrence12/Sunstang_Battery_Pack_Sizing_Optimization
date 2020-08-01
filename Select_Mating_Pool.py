import numpy as np
import pandas as pd 

def Mating_Main(Output):
    # path = r'D:\.Steven Data\Extracurricular\Sunstang\2020-2021\Strategy\Code\Output_Data'
    GG_df = pd.read_csv(Output + "\Generation Genotypes.csv")

    num_parents = 4
    parents_vel_df = []

    for parent_num in range(num_parents):

        max_fitness_idx = np.where(GG_df['ASC Score'] == np.max(GG_df['ASC Score']))

        max_fitness_idx = max_fitness_idx[0][0]
        parents_vel_df.append(pd.read_csv(Output + f'\WSC Energy Management Model({max_fitness_idx}).csv', usecols = ['Segment Velocity (km/h)']))
        
        GG_df['ASC Score'][max_fitness_idx] = -99999999999


    parents = pd.concat(parents_vel_df, axis = 1, ignore_index = True)

    parents.to_csv(Output + '\Breeding_Parents.csv', index = False, header = False)

