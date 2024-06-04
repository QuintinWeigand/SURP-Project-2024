import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as scpy

#I believe function1 is correct, this is assuming that t_naught is correct
def function_1(t_dummy, ejecta_mass):
    #print("Function1!")

    #Converts t_dummy from days to seconds
    t_dummy = t_dummy * 86400
    #print("t_dummy is:", t_dummy)
    #print("ejecta mass is:", ejecta_mass)

    #Make sure ejecta mass is converted when inputted into function

    t_naught = (0.33 * ejecta_mass) / (13.8 * 3.0e10 * 1.0e12) #This is assuming t_naught is correct
    #print("Test1:", 0.33 * ejecta_mass)
    #print("Test2:", 13.8 * 3.0e10 * 1.0e12)
    #print("t_naught is:", t_naught)

    #Note 8.8 days was turned into 760320 seconds
    instance = ((1/t_naught) * (np.exp(t_dummy/t_naught)) * (np.exp(-t_dummy/760320)))
    #print("instance is:", instance)

    return instance

#I belive function2 is correct, this is also assuming that t_naught is correct
def function_2(t_dummy, ejecta_mass):
    #print("Function2!")

    #Converts t_dummy from days to seconds
    t_dummy = t_dummy * 86400
    #print("t_dummy is:", t_dummy)
    #print("ejecta mass is:", ejecta_mass)

    #Make sure ejecta mass is converted when inputted into function

    t_naught = (0.33 * ejecta_mass) / (13.8 * 3.0e10 * 1.0e12)
    #print("Test1:", 0.33 * ejecta_mass)
    #print("Test2:", 13.8 * 3.0e10 * 1.0e12)
    #print("t_naught is:", t_naught)

    #Note 111.3 days was turned into 9616320 seconds
    instance = ((1/t_naught) * (np.exp(-t_dummy/t_naught)) * (np.exp(t_dummy/9616320)))
    #print("instance is:", instance)    

    return instance

#I believe this simpson function works
def simpson(ts_ex1, vs_ex1):
    
    area_Simp = vs_ex1[0]

    for i in range(1,len(ts_ex1)-1):
        if i%2 == 1:
            area_Simp += 4.0 * vs_ex1[i]
        else:
            area_Simp += 2.0 * vs_ex1[i]
    area_Simp += vs_ex1[-1]
        
    area_Simp *= (ts_ex1[1] - ts_ex1[0]) / 3.0

    #print(area_Simp)

    return area_Simp

def return_luminosity(t, mass_of_ejecta, Ni_mass, ejecta_velocity):
    
    t_prime = np.linspace(0, t, 1000)

    list1 = np.array([function_1(t_dummy, mass_of_ejecta) for t_dummy in t_prime])
    list2 = np.array([function_2(t_dummy, mass_of_ejecta) for t_dummy in t_prime])

    integral_1 = simpson(t_prime, list1)
    integral_2 = simpson(t_prime, list2)

    t_naught = (0.33 * mass_of_ejecta) / (13.8 * 3.0e10 * 1.0e12)
    
    part1 = (Ni_mass/t_naught * np.exp(-t/t_naught))
    part2 = (((3.9e10 - 6.8e9) * integral_1) + (6.8e9 * integral_2))
    part3 = (1 - np.exp(-((3 * .33 * mass_of_ejecta) / (4 * np.pi * (ejecta_velocity**2) * (t**2)))))
    #luminosity = (Ni_mass/t_naught * np.exp(-t/t_naught)) * ((3.9e10 - 6.8e9) * integral_1 + 6.8e9 * integral_2) * (1 - np.ext(-((3 * .33 * mass_of_ejecta) / (4 * np.pi * ejecta_velocity**2 * t**2))))
    
    luminosity = part1 * part2 * part3

    return luminosity



#Taking inputs for model and converting to CGS!

ejecta_mass = float(input("Please enter an ejecta mass (in solar mass): "))
ejecta_mass = ejecta_mass * 1.989e33
#print("Ejecta mass is:", ejecta_mass)

mass_Ni = float(input("Please enter a Ni mass (in % of ejecta mass): "))
mass_Ni = mass_Ni * ejecta_mass
#print("Ni Mass is:", mass_Ni)

ejecta_velocity = int(input("Please enter a ejecta velocity (in km/s): "))
ejecta_velocity = ejecta_velocity * 100000
#print("Ejecta Velocity is:", ejecta_velocity)



#Testing individual luminosity values
#number = return_luminosity(50, ejecta_mass, mass_Ni, ejecta_velocity)
#print(number)

#Testing full list of luminosity values
x_list = np.linspace(1,50,98)
y_list = np.array([return_luminosity(t, ejecta_mass, mass_Ni, ejecta_velocity) for t in x_list])

print(y_list)



