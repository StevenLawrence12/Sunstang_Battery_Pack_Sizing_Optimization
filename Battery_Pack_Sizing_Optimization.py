import math
import datetime
import random
import numpy as np
import pandas as pd
import os

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

def Array_Power_np(Day, Latitude, Time, Sunrise, DayLength, Pmax, Driving): #Calculate the power gain from the solar array
    SLL = 23.5*np.sin(np.radians((180*(Day-82))/182.5))
    phi_N = Latitude - SLL
    phi = 90 - ((90-phi_N)*np.sin(np.radians(180*(Time-Sunrise)/DayLength)))
    if Driving == True:
        theta = phi

    return Pmax*(np.cos(np.radians(phi))**0.3)*np.cos(np.radians(theta))

def Array_Power_np(Day, Latitude, Time, Sunrise, DayLength, Pmax, Driving): #Calculate the power gain from the solar array
    SLL = 23.5*np.sin(np.radians((180*(Day-82))/182.5))
    phi_N = Latitude - SLL
    phi = 90 - ((90-phi_N)*np.sin(np.radians(180*(Time-Sunrise)/DayLength)))
    if Driving == True:
        theta = phi

    return Pmax*(np.power(np.cos(np.radians(phi)),0.3)*np.cos(np.radians(theta)))

def Grav_Power(V,M,d,alt1,alt2): #Calculate the power loss due to gravitatational effects
    return V*M*9.81*math.sin(math.atan((alt2-alt1)/1000/d))/3.6

def Grav_Power_np(V,M,d,alt1,alt2): #Calculate the power loss due to gravitatational effects
    return V*M*9.81*np.sin(np.arctan((alt2-alt1)/1000/d))/3.6

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

def sunrise_np(latitude, longitude, timezone, year, month, day):
    latitude = np.radians(latitude)
    longitude = np.radians(longitude)

    #constants
    jd2000 = 2451545 #the julian date for Jan 1 2000 at noon
    earth_tilt = np.radians(23.44)
    sun_disc = np.radians(-0.83)

    #equations
    jd_now = date_to_jd(year,month,day) #current julian date
    n = jd_now - jd2000 + 0.0008 #Current julian day
    jstar = n - np.degrees(longitude)/360 #Mean solar noon
    M = np.radians(np.fmod(357.5291 + 0.98560028 * jstar,360)) #Solar mean anomaly - degrees
    C = 1.9148 * np.sin(M) + 0.0200 * np.sin(2*M) + 0.0003 * np.sin(3*M) #Equation of the center
    lamda = np.radians(np.fmod(np.degrees(M) + C + 180 + 102.9372,360)) #Eliptic longitude - degrees
    Jtransit = 2451545.5 + jstar + 0.0053 * np.sin(M) - 0.0069 * np.sin(2*lamda) #Solar transit
    angle_delta = np.arcsin(np.sin(lamda) * np.sin(earth_tilt)) #Deinclination of the sun
    omega = np.arccos((np.sin(sun_disc) - np.sin(latitude) * np.sin(angle_delta))/(np.cos(latitude) * np.cos(angle_delta))) #Hour angle

    Jrise = Jtransit - np.degrees(omega)/360
    Jset = Jtransit + np.degrees(omega)/360

    numdays_rise = Jrise - jd2000 +0.5 +timezone/24
    numdays_set = Jset - jd2000+0.5 +timezone/24

    sunrise = np.empty_like(numdays_rise)
    sunset = np.empty_like(numdays_rise)
    for x in range(numdays_rise.shape[0]):
        for y in range(numdays_rise.shape[1]):
            SR = datetime.datetime(2000, 1, 1) + datetime.timedelta(numdays_rise[x,y])
            SS = datetime.datetime(2000, 1, 1) + datetime.timedelta(numdays_set[x,y])
            sunrise[x,y] = (SR.hour*3600)+(SR.minute*60)+SR.second+(SR.microsecond/1000000)
            sunset[x,y] = (SS.hour*3600)+(SS.minute*60)+SS.second+(SS.microsecond/1000000)

    return sunrise, sunset

def conv_to_DT(H, M, S, MS):    #Convert time to military decimal time
    return H+(M/60)+(S/3600)+(MS/3600000000)

def Kine_Power(V_now, V_past, Dist, M, Time):
    if Time.hour == 9 and Time.minute == 0 and Time.second == 0 and Time.microsecond == 0:
        V_past = 0
    return 5.46e-7*M*9.81*(((V_now**2-V_past**2)*(V_now+V_past))/(Dist))

def Kine_Power_np(V_now, V_past, Dist, M):
    return 5.46e-7*M*9.81*(((V_now**2-V_past**2)*(V_now+V_past))/(Dist))

def P_Calc_Main(Route_Data_csv, Gen_Size):
    #Vehicle Specifications
    A = 2.38                                    #Frontal area of solar car
    Cd = 0.19                                   #Drag Coefficient of solar car
    Crr = 0.0055                                #Rolling Resistance coefficient
    Car_Mass = 375                              #Mass of solar car without passengers
    Num_Passengers = 6                          #Number of passengers in solar car
    Loaded_Weight = Car_Mass+Num_Passengers*80  #Mass of solar car with passengers
    MotEff = 0.80                               #Efficiency of the motor
    Max_Array_Power = 1300                      #Max possible power from the solar array

    #Possible Changing Variables
    p = 1.17    #density of air

    #Power Variables
    Power_elec = 50   #Power consumed from all electronics in the solar car

    #Date & Time Variables
    Start_Day = '2021-10-22T09:00:00'                       #Start day & time for race in str, will eventually be a value read from a csv file
    Time = datetime.datetime.fromisoformat(Start_Day)       #create datetime object from the Stat_Day str
    Date = Time.date()                                      #create date object from Time
    timezone = 9.5                                          #Timezone of the race, will eventually be read in from a csv file
    SR = 0                                                  #Sunrise time

    Seg_Dist = []       #distance for each segment
    EMM_Headers = ["Segment Distance (km)","Segment Velocity (km/h)","Segment Start Time","Segment Elapsed Time (s)","Segment End Time", "Array Power (W)", "Aero Power (W)", "Rolling Power (W)",
    "Gravitaional Power (W)","Kinetic Power (W)", "Battery Power (W)", "Battery Energy Consumption (kWh)"]

    Req_Datasets = Gen_Size
    # Req_Datasets = 10
    Output_path = r'D:\.Steven Data\Extracurricular\Sunstang/2020-2021\Strategy\Code\Output_Data'

    #Read route data csv file
    Route_Data_df = Route_Data_csv
    Route_Data_arr = Route_Data_df.to_numpy()
    Vel_df = pd.read_csv(Output_path + "\Velocities.csv")
    Vel_arr = Vel_df.to_numpy()


    Num_Segment = Vel_df.shape[0] #calculate the number of race route segments
    
    for x in range(Num_Segment):
        Seg_Dist.append(Haversine(Route_Data_df['latitude'][x],Route_Data_df['latitude'][x+1], Route_Data_df['longitude'][x], Route_Data_df['longitude'][x+1], 6371))

    Seg_Dist_arr = np.tile(np.reshape(np.asarray(Seg_Dist),(Num_Segment,1)),Req_Datasets)
    dT_arr = Seg_Dist_arr/Vel_arr*3600
    date_day_arr = np.full((Num_Segment, Req_Datasets),datetime.datetime.fromisoformat(Start_Day).date().day, dtype='float64')
    time_arr = np.cumsum(dT_arr, axis = 0)
    SET_arr = time_arr*(time_arr<32400)
    temp_time_arr = time_arr
    Day_arr = np.zeros((Num_Segment, Req_Datasets))
    for x in range(int(np.amax(time_arr//32400))):
        Day_arr = Day_arr + np.multiply(temp_time_arr>32400,1)
        temp_dT_arr = dT_arr*(temp_time_arr>32400)
        temp_time_arr = np.cumsum(temp_dT_arr,axis = 0)
        SET_arr = SET_arr+(temp_time_arr*(temp_time_arr<32400))
    date_day_arr += Day_arr
    Day_arr += datetime.datetime.fromisoformat(Start_Day).timetuple().tm_yday
    SET_arr += 32400
    SST_arr = SET_arr-dT_arr
    Ap_arr = Aero_Power(A, Cd, p, Vel_arr)
    Rr_arr = Roll_Resist(Crr, Vel_arr, Loaded_Weight)
    Gp_arr = Grav_Power_np(Vel_arr, Loaded_Weight, Seg_Dist_arr, Route_Data_arr[0:Num_Segment,2].reshape(Num_Segment,1), Route_Data_arr[1:Route_Data_arr.shape[0],2].reshape(Num_Segment,1))
    Sr_arr, Ss_arr = sunrise_np(Route_Data_arr[0:Num_Segment,0].reshape(Num_Segment,1), Route_Data_arr[0:Num_Segment,1].reshape(Num_Segment,1), timezone, datetime.datetime.fromisoformat(Start_Day).date().year, datetime.datetime.fromisoformat(Start_Day).date().month, date_day_arr)
    Dl_arr = Ss_arr - Sr_arr
    Ar_arr = Array_Power_np(Day_arr,Route_Data_arr[0:Num_Segment,0].reshape(Num_Segment,1), SST_arr/3600, Sr_arr/3600, Dl_arr/3600, Max_Array_Power, True)
    pVel_arr = np.concatenate((np.zeros((1,Req_Datasets)),Vel_arr[:-1,:]))
    Kp_arr = Kine_Power_np(Vel_arr, pVel_arr, Seg_Dist_arr, Loaded_Weight)
    Bp_arr = Batt_Power(Ap_arr, Rr_arr, Gp_arr, Kp_arr, Ar_arr, MotEff, Power_elec)
    BE_arr = Energy(Bp_arr, dT_arr/3600)
    
    for x in range(Req_Datasets):
        EMM_data_arr = np.concatenate((np.hsplit(Seg_Dist_arr,Req_Datasets)[x], np.hsplit(Vel_arr,Req_Datasets)[x], np.hsplit(SST_arr,Req_Datasets)[x], np.hsplit(dT_arr,Req_Datasets)[x], np.hsplit(SET_arr,Req_Datasets)[x], np.hsplit(Ar_arr,Req_Datasets)[x], 
        np.hsplit(Ap_arr,Req_Datasets)[x], np.hsplit(Rr_arr,Req_Datasets)[x], np.hsplit(Gp_arr,Req_Datasets)[x], np.hsplit(Kp_arr,Req_Datasets)[x], np.hsplit(Bp_arr,Req_Datasets)[x], np.hsplit(BE_arr,Req_Datasets)[x]), axis = 1)
        EMM_Data_df = pd.DataFrame(EMM_data_arr, columns = EMM_Headers)
        EMM_Data_df.insert(10, "Parasitic Power (W)", Power_elec)   #Adding parasitic power column of same value

        EMM_Data_df.to_csv(Output_path + f'\WSC Energy Management Model({x}).csv',index=False)       #Export EMM data to csv file
