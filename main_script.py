import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder, label_binarize
from k_nn_classification import KNNClassifier as knn
from sklearn.metrics import confusion_matrix, roc_curve, auc
from svm_classification import SVClassifier as svm
from decision_tree_classification import DTClassifier as dtc
from random_forest_classification import RFClassifier as rfc
from sklearn.feature_selection import SelectFromModel
from imblearn.over_sampling import SMOTE
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

#smote = SMOTE(sampling_strategy = 'not majority')
#
##Splitting the data into test, validation and train set
#from sklearn.model_selection import train_test_split
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)
#X_sm, y_sm = smote.fit_sample(X_train, y_train)
#y_sm = label_binarize(y_sm, [0,1,2,3,4])
#y_test = label_binarize(y_test, [0,1,2,3,4])
#n_classes = 5
#
#knn_classifier = OVRC(KNNC(n_neighbors = 5, metric = 'minkowski', p = 2)).fit(X_sm, y_sm)
#y_score_knn = knn_classifier.predict_proba(X_test)
#
#dtc_classifier = OVRC(DecisionTreeClassifier(criterion = 'entropy')).fit(X_sm, y_sm)
#y_score_dtc = dtc_classifier.predict_proba(X_test)
#
#rfc_classifier = OVRC(RandomForestClassifier(criterion = 'entropy')).fit(X_sm, y_sm)
#y_score_rfc = rfc_classifier.predict_proba(X_test)
#
#fpr_knn = dict()
#tpr_knn = dict()
#auc_knn = dict()
#for i in range(n_classes):
#    fpr_knn[i], tpr_knn[i], thresh = roc_curve(y_test[:, i], y_score_knn[:, i])
#    auc_knn[i] = auc(fpr_knn[i], tpr_knn[i])
#    
#plt.figure()
#plt.grid(True)
#plt.xlim([-0.05, 1.00])
#plt.ylim([0.0, 1.05])
#plt.plot([0, 1], [0, 1], linestyle = '--', color = 'blue')
#plt.plot(fpr_knn[2], tpr_knn[2], color = 'darkorange', label = 'ROC curve with AUC = %0.2f' %auc_knn[2])
#plt.xlabel('False Positive Rate')
#plt.ylabel('True Positive Rate')
#plt.title('Receiver Operating Characteristic Curve for Decision Tree with SMOTE')
#plt.legend(loc="lower right")
#plt.show()

#Splitting the data into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 1, test_size = 0.3)
smote = SMOTE()
X_sm, y_sm = smote.fit_sample(X_train, y_train)
rfc_1 = rfc(X_sm, y_sm)
#rfc_2 = RandomForestClassifier(criterion = 'entropy')
#selector = RFE(rfc_2, 7)
#selector.fit(X_sm, y_sm)
y_pred_1 = rfc_1.predictValues(X_test)
#y_pred_2 = selector.estimator_.predict(selector.transform(X_test))
matrix_1 = findConfusionMatrix(y_test, y_pred_1)
#matrix_2 = findConfusionMatrix(y_test, y_pred_2)
sensitivity_1 = matrix_1[2,2]/sum(matrix_1[2])
#sensitivity_2 = matrix_2[2,2]/sum(matrix_2[2])
