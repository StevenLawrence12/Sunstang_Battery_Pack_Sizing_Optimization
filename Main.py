import math
import csv
import datetime

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

def delta_T(speed,distance):
    return datetime.timedelta(hours =distance/speed)

def Batt_Power(Pdrag,Prr,Pg,Parr,MotorEff,Pelec):
    return ((Pdrag+Prr+Pg)/MotorEff)+Pelec-Parr

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
Start_Day = '2021-10-22T09:00:00'
Start_Time = datetime.datetime.fromisoformat(Start_Day)
Time = Start_Time
Date = Time.date()
timezone = 9.5
SR = 0
Max_Array_Power = 1300

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

SR = sunrise(Latitude[0], Longitude[0], timezone, Time.date())
for x in range(Num_Data): 
    Velocity.append(56.34)  #Solar Car Speed **This needs to be a list/array with a size of the number of data points along the route - 1

EMM_Data=[list(("Distance", "Velocity","delta_T","Time","Drag Power","Prr","Gravitational Power","Parasitic Power","Array Power","Battery Power","Battery Energy"))]
for x in range(Num_Data):
    dist=Haversine(Latitude[x],Latitude[x+1], Longitude[x], Longitude [x+1], 6371)
    dT= delta_T(Velocity[x],dist)
    Pd = Aero_Power(A,Cd, p, Velocity[x])
    Prr = Roll_Resist(Crr, Velocity[x], Loaded_Weight)
    Pg = Grav_Power(Velocity[x], Loaded_Weight, dist, Altitude[x], Altitude [x+1])
    Pp = 50
    Parr = Array_Power(Time.timetuple().tm_yday,Latitude[x],Time.hour+(Time.minute/60)+(Time.second/3600)+(Time.microsecond/3600000000), SR.hour +(SR.minute/60)+(SR.second/3600)+(SR.microsecond/3600000000), DL.total_seconds()/3600, Max_Array_Power, 1)
    Pbatt = Batt_Power(Pd, Prr, Pg, Parr, MotEff, Pp)
    Ebatt = Energy(Pbatt, dT.total_seconds()/3600)
    next_Time = Time+dT
    if next_Time.hour == 18:
        Time = Time.replace(day=Time.day+1, hour=9, minute=0, second=0, microsecond=0,)
        EMM_Data.append(list((dist,Velocity[x],dT.total_seconds(),Time.time(),Pd,Prr,Pg,Pp,Parr,Pbatt,Ebatt)))
        SR = sunrise(Latitude[x], Longitude[x], timezone, Time.date())
        Time = Time+dT
        continue

    EMM_Data.append(list((dist,Velocity[x],dT.total_seconds(),Time.time(),Pd,Prr,Pg,Pp,Parr,Pbatt,Ebatt)))
    Time = Time+dT


with open('WSC Energy Management Model.csv', mode = 'w', newline = '') as csv_file_write:
    EMM_writer = csv.writer(csv_file_write, delimiter = ',')
    EMM_writer.writerows(EMM_Data)
