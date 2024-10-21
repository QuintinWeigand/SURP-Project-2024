import os
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

#MinMaxScaler() is useful to normalize data where the default is  0 to 1 (aka. that is what we want)

#read the data (just read from the other file I really dont want to copy it over every time)
#make the network
#train the network
#predict the outcomes
#hyper parameterization

#This will read the data and put them into lists in memory
def read_data(filename1, filename2, ModelType="defualt_model"):
    
    x_list = []
    y_list = []

    if (ModelType == "Ni-Decay"):
        file1 = open(filename1, "r")

        for lines in file1:
            values = lines.split()

            x_list.append(values[3:])
            y_list.append(values[:3])

        file1.close()

        #Converts all the values to float
        for i in range(len(x_list)):
            for j in range(len(x_list[i])):
                x_list[i][j] = float(x_list[i][j])
        for i in range(len(y_list)):
            for j in range(len(y_list[i])):
                y_list[i][j] = float(y_list[i][j])

        x_list = np.array(x_list)
        y_list = np.array(y_list)

    elif (ModelType == "Magnetar"):
        file2 = open(filename2, "r")
        
        for lines in file2:
            values = lines.split()

            x_list.append(values[4:])
            y_list.append(values[:4])

        file2.close()
        
        for i in range(len(x_list)):
            for j in range(len(x_list[i])):
                x_list[i][j] = float(x_list[i][j])
        for i in range(len(y_list)):
            for j in range(len(y_list[i])):
                y_list[i][j] = float(y_list[i][j])

        x_list = np.array(x_list)
        y_list = np.array(y_list)
    
    else:
        raise ValueError(ModelType + " is not defined in the scope of this function. Only accepts \"Ni-Decay\" or \"Magnetar\"")
    
    return x_list, y_list

#Make sure the first arguement is Nickel Decay Model and second is Magnetar and the third reads the data for that Model
x_list, y_list = read_data(r'C:\Users\quinn\Desktop\SURP\Light_Curve_Data\0LC_data_sheet.data' ,
          r'C:\Users\quinn\Desktop\SURP\Magnetar_Light_Curve_Data\M_data_sheet.data', ModelType="Ni-Decay")


#Normalizes all the data  / creates the scalar and applys them to the data
scaler = MinMaxScaler()
x_scale = scaler.fit_transform(x_list)
#y_scale = scaler.fit_transform(y_list)

#Create a training and testing framework from total data
x_train, x_test, y_train, y_test = train_test_split(x_scale, y_list, test_size=0.20, random_state=42)

#TODO: Mess around with the parameters, see what affects it, see what doesn't, see what returns the best accuracy. 
regressor = MLPRegressor(hidden_layer_sizes= (100,), activation= "tanh", solver = "sgd", learning_rate="adaptive")

#Training the model
regressor.fit(x_train, y_train)

#Remember at this point all of the data has been scaled and needs to be unscaled after all the work is done 
y_pred = regressor.predict(x_test)

#Outputs predicted unscaled output
print(y_pred)

