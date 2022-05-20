from sklearn import svm
from sklearn import metrics
from sklearn.model_selection import train_test_split
import pandas

#Load training data
#n/a stands for normal/abnormal 
trainingData = pandas.read_csv('TrainingData.txt', names=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,"n/a"])
data = trainingData.iloc[:,0:24]
target = trainingData.loc[:,"n/a"].values

#Split training data
X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.3,random_state=13) # 70% training and 30% test

#Create a svm Classifier
clf = svm.SVC(kernel='poly', degree=4) #Polynomal kernel with a degree of 4
 
#Train the model using the training sets
clf.fit(X_train, y_train)

#Predict the label of training data
y_pred = clf.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Precision:",metrics.precision_score(y_test, y_pred))
print("Recall:",metrics.recall_score(y_test, y_pred))

#Load testing data
testingData = pandas.read_csv('TestingData.txt', names=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])

#Predict the label of testing data
test_Pred = clf.predict(testingData)

#Append labels and save to file 
testingData["n/a"] = test_Pred
print(testingData)

testingData.to_csv("TestingResults.txt", header=False, index=False)