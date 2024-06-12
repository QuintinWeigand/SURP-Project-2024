import numpy as np
import matplotlib.pyplot as plt

global Radius
Radius = 1.0e10 #in cm
global speed_of_light
speed_of_light = 3.0e10 #in cm/s

def function_1(z_dummy, B_14, P_10, ejecta_mass, ejecta_velocity, t_p, t_d, y):
    
    #Note EVERYTHING at this point should be CONVERTED to CGS

    #Math for function_1

    part1 = np.exp(z_dummy**2 + ((Radius * z_dummy) / (ejecta_velocity * t_d)))

    part2 = ( ((Radius) / (ejecta_velocity * t_d)) + z_dummy )

    part3 = ( 1 / (1 + (y * z_dummy))**2 )

    instance = part1 * part2 * part3

    return instance

def simpson(ts_ex1, vs_ex1):
    
    #Calculates the area with the data points from the lists sent
    area_Simp = vs_ex1[0]

    for i in range(1,len(ts_ex1)-1):
        if i%2 == 1:
            area_Simp += 4.0 * vs_ex1[i]
        else:
            area_Simp += 2.0 * vs_ex1[i]
    area_Simp += vs_ex1[-1]
        
    area_Simp *= (ts_ex1[1] - ts_ex1[0]) / 3.0

    #Returns the final area (the integral) to the calling environment
    return area_Simp

def return_magnetar_luminosity(t, B_14, P_10, ejecta_mass, ejecta_velocity, t_p, t_d, y, E_p):
    #Converts days to seconds
    t = t * 86400
    
    #Calculating x for the integral upper bound
    x = t / t_d
   
    #Do not need to convert time anymore since it is done above in this function
    x_prime = np.linspace(0, x, 1000)

    #Generates a list of data for function_1 to then be sent to simpson
    list1 = np.array([function_1(z_dummy, B_14, P_10, ejecta_mass, ejecta_velocity, t_p, t_d, y) for z_dummy in x_prime])

    #Generates the integral from a list of data points
    integral_1 = simpson(x_prime, list1)

    #Calculating the individual parts for the magnetar luminosity
    part1 = ((2 * E_p) / t_p) * np.exp( -( (t**2 / t_d**2) + ( (Radius * t) / (ejecta_velocity * t_d**2) ) ) )

    part2 = integral_1

    #Finally Calcualting the final magnetar luminosity
    luminosity = part1 * part2

    return luminosity


B_14 = float(input("Please enter B (in 1e14G): "))

P = float(input("Please enter P (in ms): "))
P_10 = P / 10

ejecta_velocity = int(input("Please enter a ejecta velocity (in km/s): "))
ejecta_velocity = ejecta_velocity * 100000

ejecta_mass = float(input("Please enter an ejecta mass (in solar mass): "))
ejecta_mass = ejecta_mass * 1.989e33

#Calculating important variables that are used within the functions above
t_p = 1.3 * B_14**-2 * P_10**2 #this is in years
t_p = t_p * 31536000 #converting years to seconds

t_d = np.sqrt(( 2 *.33 * ejecta_mass) / (13.8 * speed_of_light * ejecta_velocity) )

y = t_d / t_p

E_p = 2e50 / ( P_10**2 )

#Generating the lists of x points and y points
x_list = np.linspace(1,200, 398)
y_list = np.array([return_magnetar_luminosity(t, B_14, P_10, ejecta_mass, ejecta_velocity, t_p, t_d, y, E_p) for t in x_list])

#Printing the y list for comparison (most of the time commented out)
print(y_list)

#Creates the plot
fig, ax = plt.subplots()
ax.plot(x_list, y_list,
        linestyle = '-',
        color = 'black',
        linewidth = 2)

#Sets the title and x & y labels
ax.set_title('Magnetar Luminosity ( L(t) ) vs. Time (Days)')
ax.set_xlabel('Time (Days)')
ax.set_ylabel('Magnetar Luminosity ( L(t) )')

#Displays the plot
plt.show()
