import math
import csv
import datetime
import random
import numpy as np
import pandas as pd 

def Aero_Power(A, Cd, p, V): #Aerodynamic power loss calculation
    return 0.5*p*(V/3.6)**3*A*Cd

def Roll_Resist(Crr,V,M): #Calculate the power loss from friction/rolling resistance
    return Crr*(1+V/161)*M*9.81*V/3.6
 
def Array_Power(Day, Latitude, Time, Sunrise, DayLength, Pmax, Driving): #Calculate the power gain from the solar array
    SLL = 23.5*math.sin(math.radians((180*(Day-82))/182.5))
    phi_N = Latitude - SLL
    phi = 90 - ((90-phi_N)*math.sin(math.radians(180*(Time-Sunrise)/DayLength)))
    if Driving == True:
        theta = phi
    
    return Pmax*(math.cos(math.radians(phi))**0.3)*math.cos(math.radians(theta))

def Grav_Power(V,M,d,alt1,alt2): #Calculate the power loss due to gravitatational effects
    return V*M*9.81*math.sin(math.atan((alt2-alt1)/1000/d))/3.6

def Haversine(lat1, lat2, long1, long2, r):
    lat1=math.radians(lat1)
    lat2=math.radians(lat2)
    long1=math.radians(long1)
    long2=math.radians(long2)
    return 2*r*math.asin(math.sqrt(pow(math.sin((lat2-lat1)/2),2)+(math.cos(lat1)*math.cos(lat2)*pow(math.sin((long2-long1)/2),2))))

def delta_T(speed,distance):        #speed = km/h, distance = km
    return datetime.timedelta(seconds = distance/speed*3600)

def Batt_Power(Pdrag,Prr,Pg,Pk,Parr,MotorEff,Pelec):
    return ((Pdrag+Prr+Pg+Pk)/MotorEff)+Pelec-Parr

def Energy(Power, Time):
    return Power*Time/1000

def date_to_jd(year,month,day):
    # Convert a date to Julian Day.
    # Algorithm from 'Practical Astronomy with your Calculator or Spreadsheet', 
    # 4th ed., Duffet-Smith and Zwart, 2011.
    # This function extracted from https://gist.github.com/jiffyclub/1294443
    if month == 1 or month == 2:
        yearp = year - 1
        monthp = month + 12
    else:
        yearp = year
        monthp = month
    # this checks where we are in relation to October 15, 1582, the beginning
    # of the Gregorian calendar.
    if ((year < 1582) or
        (year == 1582 and month < 10) or
        (year == 1582 and month == 10 and day < 15)):
        # before start of Gregorian calendar
        B = 0
    else:
        # after start of Gregorian calendar
        A = math.trunc(yearp / 100.)
        B = 2 - A + math.trunc(A / 4.)

    if yearp < 0:
        C = math.trunc((365.25 * yearp) - 0.75)
    else:
        C = math.trunc(365.25 * yearp)
    D = math.trunc(30.6001 * (monthp + 1))
    jd = B + C + D + day + 1720994.5
    return jd    

def sunrise(latitude, longitude, timezone, date):
    latitude = math.radians(latitude)
    longitude = math.radians(longitude)
    
    #constants
    jd2000 = 2451545 #the julian date for Jan 1 2000 at noon
    earth_tilt = math.radians(23.44)
    sun_disc = math.radians(-0.83)

    #equations
    jd_now = date_to_jd(date.year,date.month,date.day) #current julian date
    n = jd_now - jd2000 + 0.0008 #Current julian day
    jstar = n - math.degrees(longitude)/360 #Mean solar noon
    M = math.radians(math.fmod(357.5291 + 0.98560028 * jstar,360)) #Solar mean anomaly - degrees
    C = 1.9148 * math.sin(M) + 0.0200 * math.sin(2*M) + 0.0003 * math.sin(3*M) #Equation of the center
    lamda = math.radians(math.fmod(math.degrees(M) + C + 180 + 102.9372,360)) #Eliptic longitude - degrees
    Jtransit = 2451545.5 + jstar + 0.0053 * math.sin(M) - 0.0069 * math.sin(2*lamda) #Solar transit
    angle_delta = math.asin(math.sin(lamda) * math.sin(earth_tilt)) #Deinclination of the sun
    omega = math.acos((math.sin(sun_disc) - math.sin(latitude) * math.sin(angle_delta))/(math.cos(latitude) * math.cos(angle_delta))) #Hour angle

    Jrise = Jtransit - math.degrees(omega)/360
    Jset = Jtransit + math.degrees(omega)/360

    numdays_rise = Jrise - jd2000 +0.5 +timezone/24
    numdays_set = Jset - jd2000+0.5 +timezone/24
    sunrise = datetime.datetime(2000, 1, 1) + datetime.timedelta(numdays_rise)
    sunset = datetime.datetime(2000, 1, 1) + datetime.timedelta(numdays_set)
    global DL 
    DL = sunset-sunrise
    return sunrise

def conv_to_DT(H, M, S, MS):    #Convert time to military decimal time
    return H+(M/60)+(S/3600)+(MS/3600000000)

def Kine_Power(V_now, V_past, Dist, M, Time): 
    if Time.hour == 9 and Time.minute == 0 and Time.second == 0 and Time.microsecond == 0:
        V_past = 0
    return 5.46e-7*M*9.81*(((V_now**2-V_past**2)*(V_now+V_past))/(Dist))

#Data sets
Route_Data_csv = input("Which competition route dataset would you like to input? ")
print(Route_Data_csv)

#Vehicle Specifications
A = 2.38                                    #Frontal area of solar car
Cd = 0.19                                   #Drag Coefficient of solar car
Crr = 0.0055                                #Rolling Resistance coefficient
Car_Mass = 300                              #Mass of solar car without passengers
Num_Passengers = 5                          #Number of passengers in solar car
Loaded_Weight = Car_Mass+Num_Passengers*80  #Mass of solar car with passengers
MotEff = 0.98                               #Efficiency of the motor
Max_Array_Power = 1300                      #Max possible power from the solar array

#Possible Changing Variables
p = 1.17    #density of air

#Power Variables
Power_Array = []    #Power obtain from the solar array 
Power_Drag = []     #Power consumed from aerodynamic drag
Power_Roll = []     #Power consumed from rolling resistance/friction
Power_Grav = []     #Power fron gravitational forces
Power_Kine = []     #Power from kinetic forces
Power_elec = 50   #Power consumed from all electronics in the solar car
Power_batt = []     #Power requirement from batteries

#Energy Variables
Energy_batt = []    #Battery energy requirement
del_Batt_E = []
Batt_E_err = 0
EMM_Data = []

#Date & Time Variables
Start_Day = '2021-10-22T09:00:00'                       #Start day & time for race in str, will eventually be a value read from a csv file
Time = datetime.datetime.fromisoformat(Start_Day)       #create datetime object from the Stat_Day str
Time_list=[]
Date = Time.date()                                      #create date object from Time
timezone = 9.5                                          #Timezone of the race, will eventually be read in from a csv file
SR = 0                                                  #Sunrise time
dT = []
deci_time = []
SST = []
SET = []

Seg_Dist = []       #distance for each segment
Velocity = []       #List of speeds for the differnce race route segments (km/h)
EMM_Headers = ["Segment Distance (km)","Segment Velocity (km/h)","Segment Start Time","Segment Elapsed Time (s)","Segment End Time", "Array Power (W)", "Aero Power (W)", "Rolling Power (W)", 
"Gravitaional Power (W)","Kinetic Power (W)", "Parasitic Power (W)", "Battery Power (W)", "Battery Energy Consumption (kWh)", "Energy Difference"]

Dataset_num = 0     #Counter for the data set number
Req_Datasets = int(input("How many datasets do you need? "))

#Criteria Variables
DataSet = []
Vel_Ave = []
Batt_E_Ave = []
Batt_E_Err = []
DCE_Headers = ["Dataset", "Velocity Average (km/h)", "Battery Energy Comsumption Average (kWh)", "Battery Energy Consumption Error Total"]
DCE_Data = []

#Read route data csv file
Route_Data_df = pd.read_csv(Route_Data_csv)
Num_Segment = len(Route_Data_df)-1 #calculate the number of race route segments

SR = sunrise(Route_Data_df['latitude'][0], Route_Data_df['longitude'][0], timezone, Time.date())
for x in range(Num_Segment): 
    Velocity.append(random.randrange(25,88))  #Solar Car Speed **This needs to be a list/array with a size of the number of data points along the route - 1]

#Calculate Powers
for x in range(Num_Segment):
    Seg_Dist.append(Haversine(Route_Data_df['latitude'][x],Route_Data_df['latitude'][x+1], Route_Data_df['longitude'][x], Route_Data_df['longitude'][x+1], 6371))
    dT.append(delta_T(Velocity[x],Seg_Dist[x]))


    End_Time = Time+dT[x]
    if End_Time.hour == 18:
        Time = Time.replace(day=Time.day+1, hour=9, minute=0, second=0, microsecond=0)
        SR = sunrise(Route_Data_df['latitude'][x], Route_Data_df['longitude'][x], timezone, Time.date())
    Time_list.append(Time)
    SST.append(Time.time())
    SET.append(Time+dT[x])
    
    Power_Array.append(Array_Power(Time.timetuple().tm_yday,Route_Data_df['latitude'][x],conv_to_DT(Time.hour,Time.minute,Time.second,Time.microsecond),conv_to_DT(SR.hour,SR.minute,SR.second,
    SR.microsecond), DL.total_seconds()/3600,Max_Array_Power,1))
    Power_Drag.append(Aero_Power(A, Cd, p, Velocity[x]))
    Power_Roll.append(Roll_Resist(Crr, Velocity[x], Loaded_Weight))
    Power_Grav.append(Grav_Power(Velocity[x], Loaded_Weight, Seg_Dist[x], Route_Data_df['altitude'][x], Route_Data_df['altitude'][x+1]))
    Power_Kine.append(Kine_Power(Velocity[x], Velocity[x-1], Seg_Dist[x], Loaded_Weight, SST[x]))
    Power_batt.append(Batt_Power(Power_Drag[x], Power_Roll[x], Power_Grav[x], Power_Kine[x], Power_Array[x], MotEff, Power_elec))
    Energy_batt.append(Energy(Power_batt[x], dT[x].total_seconds()/3600))

    Time = SET[x]
Batt_Energy_Ave = sum(Energy_batt)/len(Energy_batt)
for x in range(Num_Segment):
        del_Batt_E.append(abs(Batt_Energy_Ave-Energy_batt[x]))

#Create iterable for csv writing
EMM_Data.append(EMM_Headers)
for x in range(Num_Segment):
    EMM_Data.append(list((Seg_Dist[x], Velocity[x], SST[x], dT[x], SET[x], Power_Array[x], Power_Drag[x], Power_Roll[x], Power_Grav[x], Power_elec, Power_batt[x], 
    Energy_batt[x], del_Batt_E[x])))

#Code to change power values for each new data set
while Dataset_num != Req_Datasets:
    DataSet.append(Dataset_num)
    Time = datetime.datetime.fromisoformat(Start_Day)       #create datetime object from the Stat_Day str
    for x in range(Num_Segment): 
        Velocity[x] = random.randrange(25,88)
    for x in range(Num_Segment):
        Seg_Dist[x] = Haversine(Route_Data_df['latitude'][x],Route_Data_df['latitude'][x+1], Route_Data_df['longitude'][x], Route_Data_df['longitude'][x+1], 6371)
        dT[x] = delta_T(Velocity[x],Seg_Dist[x])


        End_Time = Time+dT[x]
        if End_Time.hour == 18:
            Time = Time.replace(day=Time.day+1, hour=9, minute=0, second=0, microsecond=0)
            SR = sunrise(Route_Data_df['latitude'][x], Route_Data_df['longitude'][x], timezone, Time.date())
        Time_list[x] = Time
        SST[x] = Time.time()
        SET[x] = Time+dT[x]
    
        Power_Array[x] = Array_Power(Time.timetuple().tm_yday,Route_Data_df['latitude'][x],conv_to_DT(Time.hour,Time.minute,Time.second,Time.microsecond),conv_to_DT(SR.hour,SR.minute,SR.second,
        SR.microsecond), DL.total_seconds()/3600,Max_Array_Power,1)
        Power_Drag[x] = Aero_Power(A, Cd, p, Velocity[x])
        Power_Roll[x] = Roll_Resist(Crr, Velocity[x], Loaded_Weight)
        Power_Grav[x] = Grav_Power(Velocity[x], Loaded_Weight, Seg_Dist[x], Route_Data_df['altitude'][x], Route_Data_df['altitude'][x+1])
        Power_Kine[x] = Kine_Power(Velocity[x], Velocity[x-1], Seg_Dist[x], Loaded_Weight, SST[x])
        Power_batt[x] = Batt_Power(Power_Drag[x], Power_Roll[x], Power_Grav[x], Power_Kine[x], Power_Array[x], MotEff, Power_elec)
        Energy_batt[x] = Energy(Power_batt[x], dT[x].total_seconds()/3600)

        Time = SET[x]

    Batt_Energy_Ave = sum(Energy_batt)/len(Energy_batt)
    #Batt_E_Ave_Txt = "Average Battery Energy Consumption for Dataset {} is: {}"
    #print(Batt_E_Ave_Txt.format(Dataset_num, Batt_Energy_Ave))
    Batt_E_Ave.append(Batt_Energy_Ave)

    Vel_Ave.append(sum(Velocity)/len(Energy_batt))
    #Vel_Ave_Txt = "Average Velocity for Dataset {} is: {}"
    #print(Vel_Ave_Txt.format(Dataset_num, Vel_Ave))
    

    for x in range(Num_Segment):
        del_Batt_E[x] = abs(Batt_Energy_Ave-Energy_batt[x])
        Batt_E_err += del_Batt_E[x]
    
    Batt_E_Err.append(Batt_E_err)
    #Batt_E_err_Txt = "Total Battery Error for Dataset {} is: {}"
    #print(Batt_E_err_Txt.format(Dataset_num, Batt_E_err))
    Batt_E_err = 0

#End of code to change power values for each new data set
    #Create iterable for csv writing
    for x in range(Num_Segment):
        EMM_Data[x+1] = list((Seg_Dist[x], Velocity[x], SST[x].strftime("%H:%M:%S%f"), dT[x].total_seconds(), SET[x].strftime("%H:%M:%S%f"), Power_Array[x], Power_Drag[x], Power_Roll[x], Power_Grav[x], Power_Kine[x], Power_elec, Power_batt[x], 
        Energy_batt[x], del_Batt_E[x]))

    WSC_EMM_CSV_name = "WSC Energy Management Model({}).csv"
    with open(WSC_EMM_CSV_name.format(Dataset_num), mode = 'w', newline = '') as csv_file_write:
        EMM_writer = csv.writer(csv_file_write, delimiter = ',')
        EMM_writer.writerows(EMM_Data)

    Dataset_num += 1
    

DCE_Data.append(DCE_Headers)
for x in range(len(DataSet)):
    DCE_Data.append(list((DataSet[x], Vel_Ave[x], Batt_E_Ave[x], Batt_E_Err[x])))

"""
with open("Dataset Critera Evalulation.csv", mode = 'w', newline = '') as csv_file_write:
    DCE_writer = csv.writer(csv_file_write, delimiter = ',')
    DCE_writer.writerows(DCE_Data)
"""