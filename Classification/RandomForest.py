from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import numpy as np
import math

x_array = []
y_array = []

file1 = open("0LC_data_sheet.data", "r")
file2 = open("M_data_sheet.data", "r")

#This is for file "0LC_data_sheet.data"
for line in file1:
    temp_list1 = []
    temp_list2 = []
    
    values = line.split()

    #temp_list1.append(values[3:]) #Grabbing the features
    
    temp_list2.append(values[0]) #Grabbing the parameters
    temp_list2.append(values[2])

    x_array.append(values[3:])
    
    y_array.append(temp_list2)

file1.close()

#This is for file "M_data_sheet.data"
for line in file2:
    temp_list1 = []
    temp_list2 = []

    values = line.split()

    #temp_list1.append(values[4:]) #Grabbing the features

    temp_list2.append(values[3]) #Grabbing the parameters
    temp_list2.append(values[2])

    x_array.append(values[4:])
    
    y_array.append(temp_list2)

file2.close()


#Converts data to a NumPy array
x_array = np.array(x_array)
y_array = np.array(y_array)


#Creates the testing and the training lists into random train and test subsets.
x_train, x_test, y_train, y_test = train_test_split(x_array, y_array, test_size=0.20, random_state=42)

#Creates a Random Forest Classifier and assigns it to forest
forest = RandomForestClassifier()

#Trains the model (forest)
forest.fit(x_train, y_train)

#Creates a prediction of y varaibles based of the trained forest model
y_pred = forest.predict(x_test)

#Outputs the accuracy of the trained data by comparing the predicted list to the correct list
print("Accuracy =", accuracy_score(y_array, y_pred))

#Shows the program is complete
print("Hello World!")