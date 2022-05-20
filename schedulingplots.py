#Importing librairies
from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def readData():
    #Reading users tasks info from the xls file
    excelFile = pd.read_excel ('COMP3217CW2Input.xlsx', sheet_name = 'User & Task ID')
    taskName = excelFile['User & Task ID'].tolist()
    readyTime = excelFile['Ready Time'].tolist()
    deadline = excelFile['Deadline'].tolist()
    maxEnergyPerHour = excelFile['Maximum scheduled energy per hour'].tolist()
    energyDemand = excelFile['Energy Demand'].tolist()
    tasks = []
    taskNames = []
    
    for k in range (len(readyTime)):
        task = []
        task.append(readyTime[k])
        task.append(deadline[k])
        task.append(maxEnergyPerHour[k])
        task.append(energyDemand[k])
        taskNames.append(taskName[k])
        
        tasks.append(task)
              
    #Reading Testing Data output
    testDF = pd.read_csv('TestingResults.txt', header=None)
    y_labels = testDF[24].tolist()
    testDF = testDF.drop(24, axis=1)
    x_data = testDF.values.tolist()
    
    return tasks, taskNames, x_data, y_labels

def createLPModel(tasks, task_names):
    '''Function to create an LP model for the scheduling problem'''

    task_vars = []
    c = []
    eq = []
    
    #creating an LP problem model for Minimization    
    model = LpProblem(name="scheduling-problem", sense=LpMinimize)
    
    #Loop over each users task
    for ind, task in enumerate(tasks):
        n = task[1] - task[0] + 1
        temp_list = []
        #Loop between ready_time and deadline for each task
        #Create LP variables with given constraints and unique names
        for i in range(task[0], task[1] + 1):
            x = LpVariable(name=task_names[ind]+'_'+str(i), lowBound=0, upBound=task[2])
            temp_list.append(x)
        task_vars.append(temp_list)

    #Create an objective function for price (to minimize) and add to the model
    for ind, task in enumerate(tasks):
        for var in task_vars[ind]:
            price = price_list[int(var.name.split('_')[2])]
            c.append(price * var)
    model += lpSum(c)
            
    #Add additional constraints to the model      
    for ind, task in enumerate(tasks):
        temp_list = []
        for var in task_vars[ind]:
            temp_list.append(var)
        eq.append(temp_list)
        model += lpSum(temp_list) == task[3]
    
    #Return model to be solved in main function
    return model

#Plot hourly energy usage for community
def plot(model, count):
    hours = [str(x) for x in range(0, 24)]
    pos = np.arange(len(hours))
    users = ['user1', 'user2', 'user3', 'user4', 'user5']
    color_list = ['blue','red','green','orange','brown']
    plot_list = []
    to_plot = []
    
    #Create lists to plot usage
    for user in users:
        temp_list = []
        for hour in hours:
            hour_list_temp = []
            task_count = 0
            for var in model.variables():
                if user == var.name.split('_')[0] and str(hour) == var.name.split('_')[2]:
                    task_count += 1
                    hour_list_temp.append(var.value())
            temp_list.append(sum(hour_list_temp))
        plot_list.append(temp_list)

    #Visualization using a bar chart stacked by user
    plt.bar(pos,plot_list[0],color=color_list[0],edgecolor=['black'],bottom=0)
    plt.bar(pos,plot_list[1],color=color_list[1],edgecolor=['black'],bottom=np.array(plot_list[0]))
    plt.bar(pos,plot_list[2],color=color_list[2],edgecolor=['black'],bottom=np.array(plot_list[0])+np.array(plot_list[1]))
    plt.bar(pos,plot_list[3],color=color_list[3],edgecolor=['black'],bottom=np.array(plot_list[0])+np.array(plot_list[1])+np.array(plot_list[2]))
    plt.bar(pos,plot_list[4],color=color_list[4],edgecolor=['black'],bottom=np.array(plot_list[0])+np.array(plot_list[1])+np.array(plot_list[2])+np.array(plot_list[3]))
    
    plt.xticks(pos, hours)
    plt.xlabel('Hour')
    plt.ylabel('Energy Usage')
    plt.title('Energy Usage Per Hour For All Users\nDay %i'%count)
    plt.legend(users,loc=0)
    plt.savefig('plots\\'+str(count)+'.png')
    plt.clf()

    return plot_list

tasks, task_names, x_data, y_labels = readData()


for ind, price_list in enumerate(x_data):
    #Schedule and plot abnormal guideline pricing curves
    if y_labels[ind] == 1:
        #Solve returned LP model fro scheduling solution
        model = createLPModel(tasks, task_names)
        answer = model.solve()
        #LP model stats
        print(answer)
        #Plot hourly usage for scheduling solution
        plot(model,ind+1)
