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

#Creating our arrays for data we wish to be entered

# TODO: B_14 is going to be replaced with t_p (NOTE Shing Chi gave parameters in days (convert to seconds))
# TODO: We have to calculate B_14 values based on our t_p
# B_14 = np.array([0.1, 0.3, 0.5, 0.7, 0.9, 1.0, 3.0, 5.0, 7.0, 9.0, 10.0, 30.0, 50.0, 70.0, 90.0, 100.0])

t_p = np.array([5.0, 10.0, 30.0, 50.0, 70.0, 100.0]) # NOTE: This is in days
P_10 = np.array([1.0, 3.0, 5.0, 7.0, 9.0, 10.0, 30.0, 50.0, 70.0, 90.0, 100.0]) #in ms
ejecta_velocity = np.array([1000.0, 3000.0, 5000.0, 7000.0, 9000.0, 10000.0, 13000.0, 15000.0, 17000.0, 19000.0, 20000.0, 23000.0, 25000.0, 27000.0, 29000.0, 30000.0])
ejecta_mass = np.array([1.0, 3.0, 6.0, 10.0, 15.0])

total_files = len(t_p) * len(P_10) * len(ejecta_velocity) * len(ejecta_mass)

print(total_files)

exit()
#Converting all the arrays to CGS (to avoid conflict in final iteration)
for i in range(len(P_10)):
    P_10[i] = P_10[i] / 10
for j in range(len(ejecta_velocity)):
    ejecta_velocity[j] = ejecta_velocity[j] * 100000
for k in range(len(ejecta_mass)):
    ejecta_mass[k] = ejecta_mass[k] * 1.989e33
for l in range(len(t_p)):
    t_p[l] = float(t_p[l]) / 365

#Creates the x_list (static for entire program)
x_list = np.linspace(1, 200, 398)

#Creates and initilized our counter that will be useful for observing during runtime

directory = r"/home/quinn/Desktop/Shing-Chi/Week3/MagnetarDB/"

counter = 1

for i in range(len(t_p)):
    
    for j in range(len(P_10)):

        # calculate B14
        print("t_p: ", t_p[0])
        B_14 = np.sqrt( (.3 * P_10[j]) / t_p[i] )
        t_p_sec = t_p[i] * 3.154e+7

        #Calculates important variables
        E_p = 2e50 / ( P_10[j]**2 )
        for k in range(len(ejecta_velocity)):

            for l in range(len(ejecta_mass)):
                
                #Creates filename based on entry data
                filename = "M_LC_" + str("{:.2f}".format(t_p[i] * 365)) + "_" + str("{:.1f}".format(P_10[j] * 10)) + "_" + str(ejecta_velocity[k] / 100000) + "_" + str(ejecta_mass[l] / 1.989e33) + ".data"

                finalLocation = directory + filename

                #Opens file
                file = open(finalLocation, "w")

                #Outputs to the console file number of total files and percentage
                print("Generating file:", counter ,"/", total_files, " ("+ "{:.2f}".format((counter / (total_files)) * 100)+ "%)" )
                
                #Calculates important variables for program
                t_d = np.sqrt(( 2 *.33 * ejecta_mass[l]) / (13.8 * speed_of_light * ejecta_velocity[k]) )

                y = t_d / t_p_sec

                #Generates the y_list
                y_list = np.array([return_magnetar_luminosity(t, B_14, P_10[j], ejecta_mass[l], ejecta_velocity[k], t_p_sec, t_d, y, E_p) for t in x_list])

                #Writes the x_list and the y_list to the file opened
                for m, (first, second) in enumerate(zip(x_list, y_list)):
                    file.write(str("{:3.1f}".format(first)) + "    " + str("{:.5e}".format(second)) + '\n')

                #Closes the file
                file.close()

                #Important runtime data to keep track
                print("Instances used:")
                print(t_p[i] * 365)
                print(P_10[j] * 10)
                print(ejecta_velocity[k] / 100000)
                print(ejecta_mass[l] /  1.989e33)

                #Increments counter
                counter += 1
            