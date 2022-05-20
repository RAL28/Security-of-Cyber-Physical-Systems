import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

#reads in the whole training data set from 'TrainingData.txt' to train the model and shuffles the order
training_data = pd.read_csv('TrainingData.txt', sep = ',', header = None)
training_data = training_data.sample(frac = 1, random_state = 49).reset_index(drop=True)
target_labels = training_data.iloc[:, -1]

#splits 70% of the training data to train the model
training_data_70 = training_data.head(7000)
target_labels_70 = training_data_70.iloc[:, -1]
training_data_70 = training_data_70.iloc[:, :24]

#splits 30% of the training data to validate the model
validation_data = training_data.tail(3000)
validation_target_labels = validation_data.iloc[:, -1]
validation_data = validation_data.iloc[:, :24]

#converts the DataFrames to NumPy arrays
training_data = np.asarray(training_data.iloc[:, :24])
training_data_70 = np.asarray(training_data_70)
target_labels = np.asarray(target_labels)
validation_data = np.asarray(validation_data)
validation_target_labels = np.asarray(validation_target_labels)

#creates and trains a multilayer perceptron classifier and prints the accuracy
MLP_clf = MLPClassifier()
MLP_clf.fit(training_data_70, target_labels_70)
MLP_results = MLP_clf.predict(validation_data)
print("Multilayer Perceptron Classifier")
print(classification_report(MLP_results, validation_target_labels))

##creates and trains a random forest classifier and prints the accuracy
RF_clf = RandomForestClassifier()
RF_clf.fit(training_data_70, target_labels_70)
RF_results = RF_clf.predict(validation_data)
print("Random Forest Classifier")
print(classification_report(RF_results, validation_target_labels))

#creates and trains a k nearest neighbours classifier and prints the accuracy
KNN_clf = KNeighborsClassifier()
KNN_clf.fit(training_data_70, target_labels_70)
KNN_results = KNN_clf.predict(validation_data)
print("K Nearest Neighbours Classifier")
print(classification_report(KNN_results, validation_target_labels))

#creates and trains a gaussian naive bayes classifier and prints the accuracy
GNB_clf = GaussianNB()
GNB_clf.fit(training_data_70, target_labels_70)
GNB_results = GNB_clf.predict(validation_data)
print("Gaussian Naive Bayes Classifier")
print(classification_report(GNB_results, validation_target_labels))

#creates and trains a support vector classifier and prints the accuracy
SVC_clf = SVC()
SVC_clf.fit(training_data_70, target_labels_70)
SVC_results = SVC_clf.predict(validation_data)
print("Support Vector Classifier")
print(classification_report(SVC_results, validation_target_labels))