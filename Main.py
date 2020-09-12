import Initialize_Population as init 
import Battery_Pack_Sizing_Optimization as BPSO
import Fit_Testing as ft
import Select_Mating_Pool as mp
import Breeding_Average_Velocity as breed
import pandas as pd
import time

Route, Generation_Size, Out_path, Velocity_df = init.main_f() 
num_generations = 100
Counter = 0

t5 = time.time()

for generations in range(num_generations):
    t0 = time.time()

    data = BPSO.P_Calc_Main(Route, Generation_Size, Out_path, Velocity_df, Counter)

    t1 = time.time()
    print("BPSO:", t1 - t0)
    
    Geno_Data = ft.FT_Main(Out_path, data, Counter)

    t2 = time.time()
    print("FT:", t2 - t1)

    Parent_Data = mp.Mating_Main(Out_path, Geno_Data, data, Counter)

    t3 = time.time()
    print("MP:", t3 - t2)

    Velocity_df = breed.Breed_Main(Out_path, Parent_Data, Counter)

    t4 = time.time()
    print("Breed:", t4 - t3)

    Counter += 1

    print("Number of iterations completed =", Counter)
    print()
    print()

t6 = time.time()
print("Time to complete program:", t6 - t5)



