import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder, label_binarize
from k_nn_classification import KNNClassifier as knn
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve
from svm_classification import SVClassifier as svm
from decision_tree_classification import DTClassifier as dtc
from random_forest_classification import RFClassifier as rfc
from sklearn.feature_selection import SelectFromModel
from imblearn.over_sampling import SMOTENC, BorderlineSMOTE
from sklearn.multiclass import OneVsRestClassifier as OVRC
from sklearn.neighbors import KNeighborsClassifier as KNNC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold, train_test_split
from sklearn.feature_selection import RFE

def findConfusionMatrix(y_test, y_pred):
    return confusion_matrix(y_test, y_pred)

# Reading the data from the source
dataset = pd.read_csv('Second Iteration Data\data_gathered_part_first_segmentation.csv', encoding = 'utf-8')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

#y = label_binarize(y, classes = [0,1,2,3,4])
#n_classes = y.shape[1]

# Encoding Categorical Features
labelEncoderTable = LabelEncoder().fit(X[:, 3])
labelEncoderMain = LabelEncoder().fit(X[:, 7])
labelEncoderArticle = LabelEncoder().fit(X[:, 8])
X[:, 3] = labelEncoderTable.transform(X[:, 3])
X[:, 7] = labelEncoderTable.transform(X[:, 7])
X[:, 8] = labelEncoderTable.transform(X[:, 8])

#X = X[:, [0, 1, 2, 4, 5, 10, 11, 13]]

smote =SMOTENC(categorical_features = [3, 7, 8], sampling_strategy = 'not majority', random_state = 42)

#Splitting the data into test, validation and train set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)
X_sm, y_sm = smote.fit_sample(X_train, y_train)
y_sm = label_binarize(y_sm, [0,1,2,3,4])
y_test = label_binarize(y_test, [0,1,2,3,4])
n_classes = 5

#knn_classifier = OVRC(KNNC(n_neighbors = 5, metric = 'minkowski', p = 2)).fit(X_sm, y_sm)
#y_score_knn = knn_classifier.predict_proba(X_test)
#
#dtc_classifier = OVRC(DecisionTreeClassifier(criterion = 'entropy')).fit(X_sm, y_sm)
#y_score_dtc = dtc_classifier.predict_proba(X_test)

rfc_classifier = OVRC(RandomForestClassifier(criterion = 'entropy')).fit(X_sm, y_sm)
y_score_rfc = rfc_classifier.predict_proba(X_test)

precision = dict()
recall = dict()
threshold = dict()
for i in range(n_classes):
    precision[i], recall[i], threshold[i] = precision_recall_curve(y_test[:, 2], y_score_rfc[:, 2])

precision["micro"], recall["micro"], threshold["micro"] = precision_recall_curve(y_test.ravel(),
    y_score_rfc.ravel())
    
plt.figure()
plt.grid(True)
plt.xlim([-0.05, 1.05])
plt.ylim([0.0, 1.05])
#plt.plot([0, 1], [0, 1], linestyle = '--', color = 'blue')
plt.plot(recall[2], precision[2], color = 'darkblue', lw = 3)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision Recall Curve for Random Forest with more data')
#plt.legend(loc="lower right")
plt.show()

#precision = []
#recall = []
#
#smote = SMOTENC(categorical_features = [3, 7, 8], sampling_strategy = 'not majority', random_state = 42)
#cross_validator = KFold(n_splits = 10, random_state = 10, shuffle = False)
#for train_index, test_index in cross_validator.split(X):
#    X_train, X_test, y_train, y_test = X[train_index], X[test_index], y[train_index], y[test_index]
#    X_sm, y_sm = smote.fit_sample(X_train, y_train)
#    rfc_classifier = rfc(X_sm, y_sm)
#    y_pred = rfc_classifier.predictValues(X_test)
#    matrix = findConfusionMatrix(y_test, y_pred)
#    if matrix.shape[0] > 2:
#        precision.append(matrix[2, 2]/sum(matrix[:, 2]))
#        recall.append(matrix[2, 2]/sum(matrix[2]))
