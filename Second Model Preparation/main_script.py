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

dataset = pd.read_csv('First Iteration Data\dataset.csv')

# Label Encoding the categorical variables
encoder = LabelEncoder()
dataset['tag_header'] = encoder.fit_transform(dataset['tag_header'].values)
dataset['tag_para'] = encoder.fit_transform(dataset['tag_para'].values)
dataset['tag_img'] = encoder.fit_transform(dataset['tag_img'].values)
dataset['attr_src'] = encoder.fit_transform(dataset['attr_src'].values)
dataset['class_image'] = encoder.fit_transform(dataset['class_image'].values)
dataset['has_listing_related'] = encoder.fit_transform(dataset['has_listing_related'].values)
dataset['tag_aside'] = encoder.fit_transform(dataset['tag_aside'].values)
dataset['class_sidebar'] = encoder.fit_transform(dataset['class_sidebar'].values)
dataset['child_img'] = encoder.fit_transform(dataset['child_img'].values)
dataset['child_text'] = encoder.fit_transform(dataset['child_text'].values)

#Transforming the variables
dataset['element_area_ratio'] = np.cbrt(dataset.element_area_ratio)
dataset['y'] = np.cbrt(dataset.y)
dataset['word_count'] = np.log(dataset.word_count)
dataset['height'] = np.cbrt(dataset.height)
dataset['width'] = np.cbrt(dataset.width)

X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

#Splitting the data into train-validation-test
X_aux, X_test, y_aux, y_test = train_test_split(X, y, random_state = 42, test_size = 0.2)
#X_train, X_validation, y_train, y_validation = train_test_split(X_aux, y_aux, test_size = 0.2)

recall_scores_knn = []
recall_scores_knn_t = []
recall_scores_dtc = []
recall_scores_dtc_t = []
recall_scores_rfc = []
recall_scores_rfc_t = []

cv = KFold(n_splits=10, random_state=42, shuffle=False)

for train_index, test_index in cv.split(X_aux):
    X_train, X_validation, y_train, y_validation = X_aux[train_index], X_aux[test_index], y_aux[train_index], y_aux[test_index]
    
    sc = StandardScaler()
    X_train[:, 7] = sc.fit_transform(X_train[:, 7].reshape(-1,1)).reshape(-1,)
    X_validation[:, 7] = sc.transform(X_validation[:, 7].reshape(-1,1)).reshape(-1,)

    knn_classifier = KNNC(X_train, y_train)
    y_pred_knn = knn_classifier.predictValues(X_validation)
    y_pred_knn_t = knn_classifier.predictValues(X_train)
    dtc_classifier = DTC(X_train, y_train)
    y_pred_dtc = dtc_classifier.predictValues(X_validation)
    y_pred_dtc_t = dtc_classifier.predictValues(X_train)
    rfc_classifier = RFC(X_train, y_train)
    y_pred_rfc = rfc_classifier.predictValues(X_validation)
    y_pred_rfc_t = rfc_classifier.predictValues(X_train)
    
    matrix_knn = confusion_matrix(y_validation, y_pred_knn)
    matrix_knn_t = confusion_matrix(y_train, y_pred_knn_t)
    
    matrix_dtc = confusion_matrix(y_validation, y_pred_dtc)
    matrix_dtc_t = confusion_matrix(y_train, y_pred_dtc_t)
    
    matrix_rfc = confusion_matrix(y_validation, y_pred_rfc)
    matrix_rfc_t = confusion_matrix(y_train, y_pred_rfc_t)
    
    recall_scores_knn.append(matrix_knn[1,1]/sum(matrix_knn[1]))
    recall_scores_knn_t.append(matrix_knn_t[1,1]/sum(matrix_knn_t[1]))
    
    recall_scores_dtc.append(matrix_dtc[1,1]/sum(matrix_dtc[1]))
    recall_scores_dtc_t.append(matrix_dtc_t[1,1]/sum(matrix_dtc_t[1]))
    
    recall_scores_rfc.append(matrix_rfc[1,1]/sum(matrix_rfc[1]))
    recall_scores_rfc_t.append(matrix_rfc_t[1,1]/sum(matrix_rfc_t[1]))