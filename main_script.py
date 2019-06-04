import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.cross_validation import train_test_split
from k_nn_classification import KNNClassifier as knn
from sklearn.metrics import confusion_matrix
from svm_classification import SVClassifier as svm
from decision_tree_classification import DTClassifier as dtc
from random_forest_classification import RFClassifier as rfc
from sklearn.feature_selection import SelectFromModel

def findConfusionMatrix(y_test, y_pred):
    return confusion_matrix(y_test, y_pred)

# Reading the data from the source
dataset = pd.read_csv('Second Iteration Data\data_gathered_part_first_segmentation.csv', encoding = 'utf-8')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# Encoding Categorical Features
labelEncoderTable = LabelEncoder().fit(X[:, 3])
labelEncoderMain = LabelEncoder().fit(X[:, 8])
labelEncoderArticle = LabelEncoder().fit(X[:, 9])
X[:, 3] = labelEncoderTable.transform(X[:, 3])
X[:, 8] = labelEncoderTable.transform(X[:, 8])
X[:, 9] = labelEncoderTable.transform(X[:, 9])

sensitivity_knn = []
sensitivity_svm = []
sensitivity_dtc = []
sensitivity_rfc = []

#
for i in range(100):
    # Splitting the data into train and test set with a 75-25 ratio
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
    
    # Fitting a K-NN Classifier to the data and observing the results
    knn_classifier = knn(X_train, y_train)
    y_pred = knn_classifier.predictValues(X_test)
    
    knnConfusionMatrix = findConfusionMatrix(y_test, y_pred)
    sensitivity_knn.append(knnConfusionMatrix[2, 2]/sum(knnConfusionMatrix[2]))

#for i in range(100):
#    # Splitting the data into train and test set with a 75-25 ratio
#    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
    
    # Fitting an SVM Classifier to the data and observing the results
    svm_classifier = svm(X_train, y_train)
    y_pred = svm_classifier.predictValues(X_test)
    
    svmConfusionMatrix = findConfusionMatrix(y_test, y_pred)
    sensitivity_svm.append(svmConfusionMatrix[2, 2]/sum(svmConfusionMatrix[2]))

#for i in range(1):
#   # Splitting the data into train and test set with a 75-25 ratio
#   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
#    
   # Fitting a Decision Tree Classifier to the data and observing the results
    dtc_classifier = dtc(X_train, y_train)
    y_pred = dtc_classifier.predictValues(X_test)

    dtcConfusionMatrix = findConfusionMatrix(y_test, y_pred)
    sensitivity_dtc.append(dtcConfusionMatrix[2, 2]/sum(dtcConfusionMatrix[2]))

#for i in range(100):
#    # Splitting the data into train and test with a 75-25 ratio
#    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

    # Fitting a Random Forest Classifier to the data and observing the results
    rfc_classifier = rfc(X_train, y_train)
    y_pred = rfc_classifier.predictValues(X_test)

    rfcConfusionMatrix = findConfusionMatrix(y_test, y_pred)
    sensitivity_rfc.append(rfcConfusionMatrix[2, 2]/sum(rfcConfusionMatrix[2]))