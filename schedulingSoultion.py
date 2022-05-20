import pandas
from scipy.optimize import linprog
import numpy as np
import matplotlib.pyplot as plt
import os

if not os.path.exists("graphs"):
    os.makedirs("graphs")

#Load testing results and input file
#n/a stands for normal/abnormal 
trainingData = pandas.read_csv('TestingResults.txt', names=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,"n/a"])
input = pandas.read_csv('COMP3217CW2Input.csv')

#Split input into users
user1 = input.iloc[0:10]
user2 = input.iloc[10:20]
user3 = input.iloc[20:30]
user4 = input.iloc[30:40]
user5 = input.iloc[40:50]
users = [user1,user2,user3,user4,user5]
userVars = []

#Filter training data to only abnormal pricing curves
abnormalCurves = trainingData.loc[trainingData["n/a"] == 1].iloc[:,0:24]
firstRow = abnormalCurves.iloc[0]


#Compute how many varibles will be needed to calculate the soultion for each user
for user in users:
    totalVars = 0
    for index, task in user.iterrows():
        for x in range(task["Ready Time"], task["Deadline"] + 1):
            totalVars += 1
    userVars.append(totalVars)

#Compute the equality constraint matricies, vectors and bounds for each user.
#These will remain the same for every calculation
As = [] #Contains all users 'a' equality constraint matricies.
Bs = [] #Contains all users 'b' equality constraint vectors.
Boundss = [] #Contains all users bounds
for userPos in range(0, len(users)):
    a = [] #The equality constraint matrix.
    b = [] #The equality constraint vector
    a_index = 0
    bounds = [] #Array of bounds
    for index, task in users[userPos].iterrows(): #Loop over each users task
        a_row = []
        for i in range(0, a_index): #Every varible that has already been defined
            a_row.append(0)
        for x in range(task["Ready Time"], task["Deadline"] + 1):
            a_index += 1
            a_row.append(1)
            bounds.append((0,1))
        for i in range(a_index, userVars[userPos]): #Varibles that still need to be defined
            a_row.append(0)
        a.append(a_row)
        b.append(task["Energy Demand"])

    As.append(a)
    Bs.append(b)
    Boundss.append(bounds)

for rowPos in range(0, len(abnormalCurves)): 
    row = abnormalCurves.iloc[rowPos]
    total = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, 21:0, 22:0, 23:0}
    
    for userPos in range(0, len(users)):
        c = [] #coefficients of the linear objective function to be minimized.
        hours = [] #Maps to result array
        for index, task in users[userPos].iterrows(): 
            for x in range(task["Ready Time"], task["Deadline"] + 1): 
                c.append(row[x]) #Set price
                hours.append(x)

        #Work out minimisation for user        
        res = linprog(c, A_eq=As[userPos], b_eq=Bs[userPos], bounds=Boundss[userPos])
        resX  = res.x
        #Add to total
        for x in range(0, len(hours)):
            total[hours[x]] += resX[x]

    #Plot
    plt.plot(total.keys(), total.values())
    plt.title("Scheduling Soultions for Abnormal Curve: " + str(rowPos+1))
    plt.xlabel("Time")
    plt.ylabel("Energy Used")
    plt.grid(True)
    plt.bar([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
    plt.savefig("graphs/" + str(rowPos+1) + ".png")
    plt.clf()