import Initialize_Population as init 
import Battery_Pack_Sizing_Optimization as BPSO
import Fit_Testing as ft
import Select_Mating_Pool as mp
import Breeding_Average_Velocity as breed

Route, Generation_Size= init.main_f() 
num_generations = 100

for generations in range(num_generations):
    BPSO.P_Calc_Main(Route, Generation_Size)
    ft.FT_Main()
    mp.Mating_Main()
    breed.Breed_Main()


