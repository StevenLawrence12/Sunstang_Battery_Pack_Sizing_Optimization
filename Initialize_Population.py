#This program is to create the inital random population of velocity values for the entire race
import pandas as pd 
import numpy as np

def main_f():
    Input_path = r'D:\.Steven Data\Extracurricular\Sunstang\2020-2021\Strategy\Code'
    Output_path = r'D:\.Steven Data\Extracurricular\Sunstang\2020-2021\Strategy\Code\Output_Data'

    num_pop = 10
    min_vel = 25
    max_vel = 120

    Vel = np.random.randint(low=min_vel,high=max_vel,size=(pd.read_csv(input("Which competition route dataset would you like to input? ")).shape[0]-1,num_pop))
    Vel_df = pd.DataFrame(Vel)
    Vel_df.to_csv(Output_path + "\Inital_Velocities.csv", index=False)