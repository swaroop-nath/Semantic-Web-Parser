from sklearn.model_selection import train_test_split, KFold
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import Pipeline
from custom_encoder import CustomEncoder
import numpy as np

#Importing the data
dataset = pd.read_csv(r'Second Iteration Data/dataset_v4.csv')
dataset = dataset.drop(['name', 'attrs'], axis = 1)
dataset = dataset.loc[~dataset['label'].isna()]
dataset = dataset.drop(['height', 'height_width_diff'], axis = 1)

#Let's look at the power of the model
X = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1]
#
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
#
model = RandomForestClassifier(n_estimators = 100, max_depth = 3)
estimators = [('encoder', CustomEncoder(['tag_header', 'tag_para', 'tag_formatting', 'tag_img', 'interacting_span_tag', 'red_flag_class', 'tag_math_span', 'src_img_interaction', 'tag_table', 'tag_sup', 'tag_unnecessary_header', 'red_flag_id'])), ('rfc', model)]
#
pipeline = Pipeline(steps = estimators)
#
#y_pred = pipeline.predict(X_test)
#
#cm = confusion_matrix(y_test, y_pred)

recall = []
precision = []
cv = KFold(n_splits=10, random_state=42, shuffle=False)
for train_index, test_index in cv.split(X.index):
#    print("Train Index: ", train_index, "\n")
#    print("Test Index: ", test_index)
    
    X_train, X_test, y_train, y_test = X.iloc[train_index], X.iloc[test_index], y.iloc[train_index], y.iloc[test_index]
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    precision.append(cm[1, 1]/(cm[0, 1] + cm[1, 1]))
    recall.append(cm[1, 1,]/(cm[1, 0] + cm[1, 1]))