#Importing libraries
import numpy as np
import matplotlib.pyplot as plt

#Declares global variables that do not change
global Radius 
Radius = 1.0e8 #in cm
global speed_of_light
speed_of_light = 3.0e10 #in cm/s

#This function is used to help generate a list for the first integral to then be integrated by simpson
def function_1(t_dummy, ejecta_mass, ejecta_velocity):
    
    #Calculates t_d
    t_d = np.sqrt(( 2 *.33 * ejecta_mass) / (13.8 * speed_of_light * ejecta_velocity) )

    #Calculates t_naught
    t_naught = (0.33 * ejecta_mass) / (13.8 * speed_of_light * Radius)

    #Calculates each part of the function (which I split into 3 parts)
    part1 = ((Radius / (ejecta_velocity * t_d)) + (t_dummy / t_d))

    part2 = np.exp((t_dummy**2/t_d**2) + ((2 * Radius * t_dummy) / (ejecta_velocity * t_d**2)))

    part3 = (np.exp(-t_dummy/760320))

    #Computes the final value
    instance = part1 * part2 * part3

    #Returns the value to the calling environment
    return instance

#This function is used to help generate a list for the second integral to then be integrated by simpson
def function_2(t_dummy, ejecta_mass, ejecta_velocity):

    #Calculates t_d
    t_d = np.sqrt(( 2 * .33 * ejecta_mass) / (13.8 * speed_of_light * ejecta_velocity))

    #Calculates t_naught
    t_naught = (0.33 * ejecta_mass) / (13.8 * speed_of_light * Radius)

    #Calculates each part of the function (which I split into 3 parts)
    part1 = ( (Radius / (ejecta_velocity * t_d) ) + (t_dummy / t_d) )
    
    part2 = np.exp( (t_dummy**2/t_d**2) + ( (2 * Radius * t_dummy) / (ejecta_velocity * t_d**2) ) )

    part3 = np.exp( -t_dummy / 9616320 )

    #Computes the final value
    instance = part1 * part2 * part3   

    #Returns the value to the calling environment
    return instance

#Function for Simpson method of integrations
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

#This function creates a list using function_1 and function_2 which calculates the integral of each and then
#computes the final luminosty at a set point
def return_luminosity(t, mass_of_ejecta, Ni_mass, ejecta_velocity):
    
    #Converts t to seconds for the final time
    t = t * 86400

    #Becuase t is now in terms of seconds we do not need to convert in the functions
    #above
    t_prime = np.linspace(0, t, 1000)

    #Creates a list for each of the inegrats to be integrated by simpson
    list1 = np.array([function_1(t_dummy, mass_of_ejecta, ejecta_velocity) for t_dummy in t_prime])
    list2 = np.array([function_2(t_dummy, mass_of_ejecta, ejecta_velocity) for t_dummy in t_prime])

    #Calculates each integral using simpson
    integral_1 = simpson(t_prime, list1)
    integral_2 = simpson(t_prime, list2)

    #Calculates t_d
    t_d = np.sqrt( ( 2 *.33 * ejecta_mass) / (13.8 * speed_of_light * ejecta_velocity) )

    #Calculates t_naught
    t_naught = (0.33 * mass_of_ejecta) / (13.8 * speed_of_light * Radius)
    
    #Calculates each part of the total function (which I split into 3 parts)
    part1 = (2*Ni_mass/t_d * np.exp(-(t**2/t_d**2) + (2 * Radius * t) / (ejecta_velocity * t_d**2)))

    part2 = (((3.9e10 - 6.8e9) * integral_1) + (6.8e9 * integral_2))

    part3 = (1 - np.exp(-((3 * .33 * mass_of_ejecta) / (4 * np.pi * (ejecta_velocity**2) * (t**2)))))
    
    #Calculates the final luminosity using the 3 parts
    luminosity = part1 * part2 * part3

    #Return luminosity to the calling environment
    return luminosity

#Starting points for the generating data
ejecta_mass = 0.8
mass_Ni = 0.1
ejecta_velocity = 1000
leave = False

while(leave == False):
    #Taking inputs for model
    #ejecta_mass = float(input("Please enter an ejecta mass (in solar mass): "))

    #mass_Ni = float(input("Please enter a Ni mass (fraction of ejecta mass): "))

    #ejecta_velocity = int(input("Please enter a ejecta velocity (in km/s): "))


    #Creates a data file based on variable entry
    filename = "LC_" + str("{:.2f}".format(ejecta_mass)) + "_" + str("{:.1f}".format(mass_Ni)) + "_" + str(int(ejecta_velocity)) + ".data"

    #Converting the data to CGS
    ejecta_mass = ejecta_mass * 1.989e33
    mass_Ni = mass_Ni * ejecta_mass
    ejecta_velocity = ejecta_velocity * 100000


    #Testing individual luminosity values
    #number = return_luminosity(50, ejecta_mass, mass_Ni, ejecta_velocity)
    #print("Luminosity is =", number)

    #Testing full list of luminosity values
    x_list = np.linspace(1,200,398)
    y_list = np.array([return_luminosity(t, ejecta_mass, mass_Ni, ejecta_velocity) for t in x_list])

    #Prints the y values
    #print(y_list)



    #Opens the file in write mode
    file = open(filename, "w")

    #Writes the data to the file
    for i, (x, y) in enumerate(zip(x_list, y_list)):
        file.write(str("{:3.1f}".format(x)) + "    " + str("{:.5e}".format(y)) + '\n')

    #Converting back
    print("\nParameters used:\n")
    mass_Ni = mass_Ni / ejecta_mass
    ejecta_mass = ejecta_mass / 1.989e33
    print("Ejecta_mass =", str("{:.2f}".format(ejecta_mass)))
    print("mass_Ni =", str("{:.1f}".format(mass_Ni)))
    ejecta_velocity = ejecta_velocity / 100000
    print("Ejecta_velocity =", ejecta_velocity)

    ejecta_velocity += 1000

    file.close()
    
    #The last points we want for the data range (ejecta_velocity is the iterator so once its above we know were done)
    if (ejecta_mass == 1.4 and mass_Ni == 0.9 and ejecta_velocity > 20000):
        leave = True
    else:
        if (ejecta_velocity > 20000):
            mass_Ni += 0.1
            ejecta_velocity = 1000
        if (mass_Ni > 0.99):
            ejecta_mass += 0.05
            mass_Ni = 0.1

    #ejecta_velocity += 1000

print("\n\n\n\n\nPROGRAM FINISHED!!!\n\n\n\n")


#Creates the plot
#fig, ax = plt.subplots()
#ax.plot(x_list, y_list,
#        linestyle = '-',
#        color = 'black',
#        linewidth = 2)

#Sets the title and x & y labels
#ax.set_title('Luminosity ( L(t) ) vs. Time (Days)')
#ax.set_xlabel('Time (Days)')
#ax.set_ylabel('Luminosity ( L(t) )')

#Displays the plot
#plt.show()
