import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.cross_validation import train_test_split
from k_nn_classification import KNN as knn
from sklearn.metrics import confusion_matrix

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

accuracy = []

for i in range(1000):
    # Splitting the data into train and test set with a 75-25 ratio
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
    
    # Fitting a K-NN Classifier to the data and observing the results
    classifier = knn(X_train, y_train)
    y_pred = classifier.predictValues(X_test)
    
    knnConfusionMatrix = findConfusionMatrix(y_test, y_pred)
    accuracy.append(sum(np.diagonal(knnConfusionMatrix))/sum(sum(knnConfusionMatrix)))