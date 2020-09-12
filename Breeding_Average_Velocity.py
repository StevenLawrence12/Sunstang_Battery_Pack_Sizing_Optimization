import numpy as np
import pandas as pd 
from itertools import combinations
import random

def Breed_Main(Generation_Size):
    mut_prob = .05
    min_vel = 25
    max_vel = 120
    # mut_loc = []
    path = r'D:\.Steven Data\Extracurricular\Sunstang\2020-2021\Strategy\Code\Output_Data'
    Parent_vel_df = pd.read_csv(path + "\Breeding_Parents.csv", header=None)
    Combinations = list(combinations(range(Parent_vel_df.shape[1]),2))
    num_parents = int(0.2*Generation_Size) # number of parents calculation
    offspring_num = Generation_Size - num_parents

    par_vel_arr = Parent_vel_df.to_numpy()
    off_vel_arr = np.empty([Parent_vel_df.shape[0], offspring_num])

    for x in range(offspring_num):
        P1_idx = Combinations[x][0]
        P2_idx = Combinations[x][1]
        
        for vel in range(Parent_vel_df.shape[0]):
            off_vel_arr[vel][x] = (Parent_vel_df.iloc[vel,P1_idx]+Parent_vel_df.iloc[vel,P2_idx])/2
            if random.random() < mut_prob:
                off_vel_arr[vel][x] = random.randrange(min_vel, max_vel)
    #             mut_loc.append((vel,x))

    # mut_loc_arr = np.asarray(mut_loc)

    new_gen_df = pd.DataFrame(np.concatenate((par_vel_arr,off_vel_arr),axis=1))
    new_gen_df.to_csv(path + r"\Velocities.csv", index=False)
