import math
import csv
import time

def Aero_Power(A, Cd, p, V): #Aerodynamic power loss calculation
    return 0.5*p*(V/3.6)**3*A*Cd

def Roll_Resist(Crr,V,M): #Calculate the power loss from friction/rolling resistance
    return Crr*(1+V/161)*M*9.81*V/3.6

def Array_Power(): #Calculate the power gain from the solar array
    pass

def Grav_Power(V,M,d,alt1,alt2): #Calculate the power loss due to gravitatational effects
    return V*M*9.81*math.sin(math.atan((alt2-alt1)/1000/d))/3.6

def Haversine(lat1, lat2, long1, long2, r):
    lat1=math.radians(lat1)
    lat2=math.radians(lat2)
    long1=math.radians(long1)
    long2=math.radians(long2)
    return 2*r*math.asin(math.sqrt(pow(math.sin((lat2-lat1)/2),2)+(math.cos(lat1)*math.cos(lat2)*pow(math.sin((long2-long1)/2),2))))

def delta_T(speed,distance):
    return distance/speed

def Batt_Power(Pdrag,Prr,Pg,Parr,MotorEff,Pelec):
    return ((Pdrag+Prr+Pg)/MotorEff)+Pelec-Parr

def Energy(Power, Time):
    return Power*Time/1000

#Vehicle Specifications
A = 2.38    #Frontal area of solar car
Cd = 0.19   #Drag Coefficient of solar car
Crr = 0.0055    #Rolling Resistance coefficient
Car_Mass = 300  #Mass of solar car without passengers
Num_Passengers = 5  #Number of passengers in solar car
Loaded_Weight = Car_Mass+Num_Passengers*80  #Mass of solar car with passengers
MotEff = 0.98

#Possible Changing Variables
p = 1.17    #density of air

#Changing Variables
Velocity = []
Latitude = []
Longitude = []
Altitude = []


with open('WSC Route Data.csv') as csv_file:
    routeReader = csv.reader(csv_file,delimiter = ',')
    lineCount=0
    for row in routeReader:
        if lineCount == 0:
            lineCount += 1
            continue
        Latitude.append(float(row[0]))
        Longitude.append(float(row[1]))
        Altitude.append(float(row[2]))
        lineCount += 1

Num_Data = lineCount-2

for x in range(Num_Data): 
    Velocity.append(56.34)  #Solar Car Speed **This needs to be a list/array with a size of the number of data points along the route - 1

EMM_Data=[list(("Distance", "Velocity","Time","Drag Power","Prr","Gravitational Power","Parasitic Power","Array Power","Battery Power","Battery Energy"))]
for x in range(Num_Data):
    dist=Haversine(Latitude[x],Latitude[x+1], Longitude[x], Longitude [x+1], 6371)
    time = delta_T(Velocity[x],dist)
    Pd = Aero_Power(A,Cd, p, Velocity[x])
    Prr = Roll_Resist(Crr, Velocity[x], Loaded_Weight)
    Pg = Grav_Power(Velocity[x], Loaded_Weight, dist, Altitude[x], Altitude [x+1])
    Pp = 50
    Parr = 500
    Pbatt = Batt_Power(Pd, Prr, Pg, Parr, MotEff, Pp)
    Ebatt = Energy(Pbatt, time)
    EMM_Data.append(list((dist,Velocity[x],time,Pd,Prr,Pg,Pp,Parr,Pbatt,Ebatt)))

with open('WSC Energy Management Model.csv', mode = 'w', newline = '') as csv_file_write:
    EMM_writer = csv.writer(csv_file_write, delimiter = ',')
    EMM_writer.writerows(EMM_Data)