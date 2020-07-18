import numpy as np
import pandas as pd 
from itertools import combinations
import random

mut_prob = .05
min_vel = 25
max_vel = 120
mut_loc = []
Parent_vel_df = pd.read_csv('Breeding_Parents.csv', header=None)
Combinations = list(combinations(range(Parent_vel_df.shape[1]),2))
offspring_num = len(Combinations)

par_vel_arr = Parent_vel_df.to_numpy()
off_vel_arr = np.empty([Parent_vel_df.shape[0], offspring_num])

for x in range(offspring_num):
    P1_idx = Combinations[x][0]
    P2_idx = Combinations[x][1]
    
    for vel in range(Parent_vel_df.shape[0]):
        off_vel_arr[vel][x] = (Parent_vel_df.iloc[vel,P1_idx]+Parent_vel_df.iloc[vel,P2_idx])/2
        if random.random() < mut_prob:
            off_vel_arr[vel][x] = random.randrange(min_vel, max_vel)
            mut_loc.append((vel,x))

mut_loc_arr = np.asarray(mut_loc)
print(mut_loc_arr)
print(mut_loc_arr.shape)



new_gen_df = pd.DataFrame(np.concatenate((par_vel_arr,off_vel_arr),axis=1))

new_gen_df.to_csv('New_Generation.csv', index=False)
