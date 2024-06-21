import os
import numpy as np
import matplotlib.pyplot as plt

#list1 = os.listdir()
#list1.remove("testing.py") #or the filename of the python code

def read_data_from_file(filename):
    x_list = []
    y_list = []
    
    #I belive since we are using "as" then we do not need to close the file but just in case 
    #I will close the file below
    with open(filename, 'r') as file:
        for line in file:
            #Splits the line into two
            values = line.split()
            if len(values) == 2:
                x_list.append(float(values[0]))
                y_list.append(float(values[1]))

    #Makes sure the file that is being read is closed
    file.close()
    
    return x_list, y_list

def coef_of_variation(standard_deviation, mean):
    return (standard_deviation / mean)

def skew(y_list, mean, standard_deviation):
    
    sum = 0

    for i in range(len(y_list)):
        sum += ( (y_list[i] - mean)**3 ) 

    skew = sum / ( (len(y_list) - 1) * (standard_deviation**3) )
    
    return skew

def kurtosis(y_list, mean):
    
    top_sum = 0
    bot_sum = 0
    n = len(y_list)

    for i in range(len(y_list)):
        top_sum += ( (y_list[i] - mean)**4 ) 
        bot_sum += ( (y_list[i] - mean)**2 )
    
    #print("top sum =", top_sum, "\nbot sum =", bot_sum)

    kurtosis = (n * top_sum) / (bot_sum**2)
    
    return kurtosis

def MAD(y_list, median):
    
    temp_list = []
    
    for i in range(len(y_list)):
        temp_list.append(np.absolute(y_list[i] - median))
    
    #print("Printing temp list:\n", temp_list)
    
    return np.median(temp_list)

def deltaL15(x_list, y_list, maximum):
    
    x_point_max = y_list.index(maximum)

    if ( x_point_max + 30 > (len(y_list) - 1) ):
        L_15 = y_list[-1]
    else:
        L_15 = y_list[x_point_max + 30]

    return (np.log(L_15 / maximum))

#Temporary will use os.listdict() for handeling the filenames and iterate through
#filename = "LC_0.8_5_1000.0.data"



filelist = os.listdir()
filelist.remove("0LC_data_gen.py")
filelist.remove("data_reader.py")


file = open("0LC_data_sheet.data", "w")

for i in range(len(filelist)):

    ejecta_mass = None
    Ni_mass = None
    ejecta_velocity = None

    print("Filename for current instance:", filelist[i])
    filename_elements = filelist[i].split("_")

    #This is so the testing files I make do not break the program, this can be removed shortly once everything is set
    if (len(filename_elements) > 2):
        filename_elements[-1] = filename_elements[-1].removesuffix(".data")

        #Reads the variables for the data used into memory can be used 
        #which will be used to output to a file
        ejecta_mass = filename_elements[1]
        Ni_mass = filename_elements[2]
        ejecta_velocity = filename_elements[3]


    x_list, y_list = read_data_from_file(filelist[i])

    #print(y_list)

    #defines important non changing varaibles (max, standard deviation, mean, etc.)
    maximum = np.max(y_list)
    mean = np.mean(y_list)
    median = np.median(y_list)
    standard_deviation = np.std(y_list)

    #print("Maximum =", maximum)
    #print("Mean =", mean)
    #print("Median =", median)
    #print("Standard Deviation =", standard_deviation)

    #print("\nThe five important data points:")
    #print("The maximum peak =", maximum)
    #print("Coefficient Of Variation =", coef_of_variation(standard_deviation, mean))
    #print("Skew =", skew(y_list, mean, standard_deviation))
    #print("Kurtosis =", kurtosis(y_list, mean))
    #print("Median Absolute Deviation =", MAD(y_list, median))

    file.write(str(ejecta_mass) + " " + str(Ni_mass) + " " + str(ejecta_velocity) + " ")
    #file.write(str(maximum) + " " + str(coef_of_variation(standard_deviation, mean)) + " " + str(skew(y_list, mean, standard_deviation)) + " ")
    #file.write(str(kurtosis(y_list, mean)) + " " + str(MAD(y_list, median)) + " " + str(deltaL15(x_list,y_list,maximum)) + "\n")

    file.write(str("{:.5e}".format(maximum)) + " " + str("{:.5f}".format(coef_of_variation(standard_deviation, mean))) + " ")
    file.write(str("{:.5f}".format(skew(y_list, mean, standard_deviation))) + " " + str("{:.5f}".format(kurtosis(y_list, mean))) + " ")
    file.write(str("{:.5e}".format(MAD(y_list, median))) + " " + str("{:.5f}".format(deltaL15(x_list, y_list, maximum))) + "\n")

file.close()

#fig, ax = plt.subplots()
#ax.plot(x_list, y_list, linestyle = '-', color = 'black', linewidth = 2)

#plt.show()