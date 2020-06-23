import math
import csv

with open('WSC Route Data.csv') as csv_file:
    routeReader = csv.reader(csv_file,delimiter = ',')
    lineCount=0
    for row in routeReader:
        if lineCount == 0:
            DataPoints = [tuple((row[0],row[1],row[2]))]
            lineCount+=1
        else:
            DataPoints.append(tuple((float(row[0]),float(row[1]),float(row[2]))))

    
#for x in range(len(DataPoints)):
    #EMM_writer.writerow()
        
#for x in DataPoints:
#    print(x[0],x[1],x[2])      

print(len(DataPoints))

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
    return Power*Time
    
A = 2.38    #Frontal area of solar car
Cd = 0.19   #Drag Coefficient of solar car
p = 1.17    #density of air
V=list((56.34,))

for x in range(len(DataPoints)-1): 
    V.append(56.34)  #Solar Car Speed **This needs to be a list/array with a size of the number of data points along the route - 1

print(type(V))

print(len(V))
Crr = 0.0055    #Rolling Resistance coefficient
Car_Mass = 300  #Mass of solar car without passengers
Num_Passengers = 5  #Number of passengers in solar car
Loaded_Weight = Car_Mass+Num_Passengers*80  #Mass of solar car with passengers
MotEff = 0.98

print(Loaded_Weight)
#print(Aero_Power(A,Cd,p,V))
#print(Roll_Resist(Crr,V,713.5575943))
print(Haversine(39.09215,39.09216,-94.41626,-94.41639,6371))
print(Grav_Power(56.34,713.5575943,Haversine(39.09215,39.09216,-94.41626,-94.41639,6371),319.1,319.4))

EMM_Data=[list(("Distance", "Velocity","Time","Drag Power","Prr","Gravitational Power","Parasitic Power","Array Power","Battery Power","Battery Energy"))]

with open('WSC Energy Management Model.csv', mode = 'w', newline = '') as csv_file_write:
    EMM_writer = csv.writer(csv_file_write, delimiter = ',')
    EMM_writer.writerows(EMM_Data)