from sklearn.preprocessing import LabelEncoder
from random_forest_classification import RFClassifier as RFC
import pandas as pd
import numpy as np
import pickle

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
dataset['tag_elem'] = encoder.fit_transform(dataset['tag_elem'].values)
dataset['red_flag_id'] = encoder.fit_transform(dataset['red_flag_id'].values)

dataset['height_width_diff'] = np.cbrt(dataset['height_width_diff'].values)

#Transforming the variables
data = dataset.iloc[:, :-2]
data['tag_header_y_interacted'] = np.multiply(data['tag_header'], data['relative_y_coord'])
data['span_interaction_y_interacted'] = np.multiply(data['interacting_span_tag'], data['relative_y_coord'])
data['tag_para_y_interacted'] = np.multiply(data['tag_para'], data['relative_y_coord'])
data = data.drop(['tag_dl_type', 'tag_math_type', 'tag_math_elem', 'tag_annotation'], axis = 1)
X = data.iloc[:, :-1].values
y = data.iloc[:, 19].values

model = RFC(X, y)
pickle.dump(model, open("second_classifier.pkl", "wb"))