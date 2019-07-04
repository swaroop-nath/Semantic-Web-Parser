from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, KFold
import seaborn as sns
from matplotlib import pyplot as plt
from k_nn_classification import KNNClassifier as KNNC
from decision_tree_classification import DTClassifier as DTC
from random_forest_classification import RFClassifier as RFC
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTENC

dataset = pd.read_csv('First Iteration Data\dataset.csv')

# Label Encoding the categorical variables
encoder = LabelEncoder()
dataset['tag_header'] = encoder.fit_transform(dataset['tag_header'].values)
dataset['tag_para'] = encoder.fit_transform(dataset['tag_para'].values)
dataset['tag_formatting'] = encoder.fit_transform(dataset['tag_formatting'].values)
dataset['interacting_span_tag'] = encoder.fit_transform(dataset['interacting_span_tag'].values)
dataset['tag_img'] = encoder.fit_transform(dataset['tag_img'].values)
dataset['src_img_interaction'] = encoder.fit_transform(dataset['src_img_interaction'].values)
dataset['red_flag_class'] = encoder.fit_transform(dataset['red_flag_class'].values)
dataset['tag_table'] = encoder.fit_transform(dataset['tag_table'].values)
dataset['tag_sup'] = encoder.fit_transform(dataset['tag_sup'].values)
dataset['tag_sup_child'] = encoder.fit_transform(dataset['tag_sup_child'].values)
dataset['red_flag_id'] = encoder.fit_transform(dataset['red_flag_id'].values)

#Transforming the variables
data = dataset.iloc[:, :-2]
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

X[:, -1] = np.cbrt(X[:,-1])
#smote = SMOTENC(random_state = 42, categorical_features = [0,1,2,4,9,10,11,12,13,14,15])

#Splitting the data into train-validation-test
X_aux, X_test, y_aux, y_test = train_test_split(X, y, random_state = 42, test_size = 0.2)
X_train, X_validation, y_train, y_validation = train_test_split(X_aux, y_aux, random_state = 42, test_size = 0.2)

#recall_scores_knn = []
#recall_scores_knn_t = []
#recall_scores_dtc = []
#recall_scores_dtc_t = []
#recall_scores_rfc = []
#recall_scores_rfc_t = []
#
#cv = KFold(n_splits=10, random_state=42, shuffle=False)
#
#for train_index, test_index in cv.split(X_aux):
#    X_train, X_validation, y_train, y_validation = X_aux[train_index], X_aux[test_index], y_aux[train_index], y_aux[test_index]
#
#    X_train, y_train = smote.fit_resample(X_train, y_train)
#    knn_classifier = KNNC(X_train, y_train)
#    y_pred_knn = knn_classifier.predictValues(X_validation)
#    y_pred_knn_t = knn_classifier.predictValues(X_train)
#    dtc_classifier = DTC(X_train, y_train)
#    y_pred_dtc = dtc_classifier.predictValues(X_validation)
#    y_pred_dtc_t = dtc_classifier.predictValues(X_train)
#    rfc_classifier = RFC(X_train, y_train)
#    y_pred_rfc = rfc_classifier.predictValues(X_validation)
#    y_pred_rfc_t = rfc_classifier.predictValues(X_train)
#    
#    matrix_knn = confusion_matrix(y_validation, y_pred_knn)
#    matrix_knn_t = confusion_matrix(y_train, y_pred_knn_t)
#    
#    matrix_dtc = confusion_matrix(y_validation, y_pred_dtc)
#    matrix_dtc_t = confusion_matrix(y_train, y_pred_dtc_t)
#    
#    matrix_rfc = confusion_matrix(y_validation, y_pred_rfc)
#    matrix_rfc_t = confusion_matrix(y_train, y_pred_rfc_t)
#    
#    recall_scores_knn.append(matrix_knn[1,1]/sum(matrix_knn[1]))
#    recall_scores_knn_t.append(matrix_knn_t[1,1]/sum(matrix_knn_t[1]))
#    
#    recall_scores_dtc.append(matrix_dtc[1,1]/sum(matrix_dtc[1]))
#    recall_scores_dtc_t.append(matrix_dtc_t[1,1]/sum(matrix_dtc_t[1]))
#    
#    recall_scores_rfc.append(matrix_rfc[1,1]/sum(matrix_rfc[1]))
#    recall_scores_rfc_t.append(matrix_rfc_t[1,1]/sum(matrix_rfc_t[1]))

def findEquality(i, x):
    if X_validation[x, -1] == dataset.height_width_diff[i] and X_validation[x, 5] == dataset.relative_x_coord[i] and X_validation[x, 6] == dataset.relative_y_coord[i]: return True
    else: return False

def findFaultyCases(y_true, y_pred):
    faulty_indices = []
    faulty_cases = []
    for i in range(len(y_pred)):
        if y_true[i] != y_pred[i]: faulty_indices.append(i)
    print(len(faulty_indices))
    for x in faulty_indices:
        for i in range(dataset.shape[0]):
            if findEquality(i, x): faulty_cases.append(i)
        
    return faulty_cases

rfc_classifier = RFC(X_train, y_train)
y_pred = rfc_classifier.predictValues(X_validation)
faults = findFaultyCases(y_validation, y_pred)
matrix = confusion_matrix(y_validation, y_pred)