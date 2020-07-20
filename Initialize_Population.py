#This program is to create the inital random population of velocity values for the entire race
import pandas as pd 
import numpy as np

def main_f():
    Input_path = r'D:\.Steven Data\Extracurricular\Sunstang\2020-2021\Strategy\Code'
    Output_path = r'D:\.Steven Data\Extracurricular\Sunstang\2020-2021\Strategy\Code\Output_Data'

    num_pop = 10
    min_vel = 25
    max_vel = 120

    Route_Data_df = pd.read_csv(input("Which competition route dataset would you like to input? "))
    Generation_Size = int(input("How many datasets do you need? "))
    Vel = np.random.randint(low=min_vel,high=max_vel,size=(Route_Data_df.shape[0]-1,num_pop))
    Vel_df = pd.DataFrame(Vel)
    Vel_df.to_csv(Output_path + "\Velocities.csv", index=False)

    return Route_Data_df, Generation_Size