import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, LogLocator, AutoMinorLocator)

#Function for splitting the line and writting it to two lists
def read_data_from_file(filename):
    x_list = []
    y_list = []
    
    with open(filename, 'r') as file:
        for line in file:
            #Splits the line into two
            values = line.split()
            if len(values) == 2:
                x_list.append(float(values[0]))
                y_list.append(float(values[1]))
    
    return x_list, y_list

B_14 = float(input("Please enter B (in 1e14G): "))

P = float(input("Please enter P (in ms): "))

ejecta_velocity = float(input("Please enter a ejecta velocity (in km/s): "))

ejecta_mass = float(input("Please enter an ejecta mass (in solar mass): "))

#Creates a file name to compare to existing files
filename = "M_LC_" + str("{:.2f}".format(B_14)) + "_" + str("{:.1f}".format(P)) + "_" + str("{:.1f}".format(ejecta_velocity)) + "_" + str("{:.1f}".format(ejecta_mass)) + ".data"

#Trys to open the file if it cannot be done terminate the program
try:
    file = open(filename, "r")
except FileNotFoundError:
    print("A file with those parameters was not found!")
    exit()
else:
    print("The file was found!")

#Creates the x and y list
x_list, y_list = read_data_from_file(filename)

#Converts the lists to numpy arrays
x_list = np.array(x_list)
y_list = np.array(y_list)

#Creates the plot
fig, ax = plt.subplots()
ax.plot(x_list, y_list,
        linestyle = '-',
        color = 'black',
        linewidth = 2)

#Sets the title and x & y labels
ax.set_title('Magnetar - Luminosity ( L(t) ) vs. Time (Days)')
ax.set_xlabel('Time (Days)')
ax.set_ylabel('Magnetar - Luminosity ( L(t) )')

ax.xaxis.set_minor_locator(MultipleLocator(5)) #change 0.1 to the appropriate number for your minor ticks
ax.yaxis.set_minor_locator(LogLocator(10)) #change 10 to the appropriate number for your minor ticks 

ax.tick_params(which="major", length=8)
ax.tick_params(which="minor", length=4)

ax.xaxis.set_ticks_position("both")
ax.yaxis.set_ticks_position("both")

print(y_list)

#Displays the plot
plt.show()


