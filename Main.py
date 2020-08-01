import Initialize_Population as init 
import Battery_Pack_Sizing_Optimization as BPSO
import Fit_Testing as ft
import Select_Mating_Pool as mp
import Breeding_Average_Velocity as breed

Route, Generation_Size, Out_path = init.main_f() 
num_generations = 100

for generations in range(num_generations):
    BPSO.P_Calc_Main(Route, Generation_Size, Out_path)
    ft.FT_Main(Out_path)
    mp.Mating_Main(Out_path)
    breed.Breed_Main(Out_path)


