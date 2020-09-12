import numpy as np          #numpy module to use arrays
import pandas as pd         #pandas library to easilt import and export csv/excel files
import glob                 #Used to read the multiple excel files containing each individual comp simulation

def ASC_Scoring (T, E, D):  
    return D/E*T

def Target_Speed_Derate(V):     #V = km/h
    V = V/1.60934
    if V < 35:
        T = 0.4**(35-V)
    else:
        T = 1

    return T

def FT_Main(Output, Data_Frames, Counter):
    #Prepare to read multiple csv files
    # path = r'D:\.Steven Data\Extracurricular\Sunstang\2020-2021\Strategy\Code\Output_Data'
    # filenames = glob.glob(Output + "\WSC Energy*.csv")

    # dfs = [pd.read_csv(f) for f in filenames] #reading all the csv energy management model files

    Headers = np.array([['Data Set #', 'Average Velocity (km/h)', 'Total Battery Energy Consumption (kWh)','Target Speed Derate','ASC Score']]) # All the criteria that we are using to determine each indiviudals fitness 
    Genotype_array = np.empty((0, np.size(Headers, axis = 1))) #Creating an empty array for all the genotypes

    for x in range(len(Data_Frames)): #Calculating all the genotype values for each dataset
        Genotype_array = np.append(Genotype_array, [[x, Data_Frames[x]['Segment Velocity (km/h)'].mean(), Data_Frames[x]['Battery Energy Consumption (kWh)'].sum(), Target_Speed_Derate(Data_Frames[x]['Segment Velocity (km/h)'].mean()),
        ASC_Scoring(Target_Speed_Derate(Data_Frames[x]['Segment Velocity (km/h)'].mean()), Data_Frames[x]['Battery Energy Consumption (kWh)'].sum(), 5*Data_Frames[x]['Segment Distance (km)'].sum())]], axis = 0)

    Genotype_df = pd.DataFrame(Genotype_array, columns = Headers[0,:]) #converting the numpy array to a pandas dataframe

    if Counter == 99:
        Genotype_df.to_csv(Output + "\Generation Genotypes.csv", index = False)       #export the dataframe to a csv file

    return Genotype_df

    # Genotype_df.to_csv(Output + "\Generation Genotypes.csv", index = False)       #export the dataframe to a csv file