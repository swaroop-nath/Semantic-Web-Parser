from sklearn.preprocessing import LabelEncoder
from random_forest_classification import RFClassifier as RFC
import pandas as pd
import numpy as np
import pickle

dataset = pd.read_csv(r'First Iteration Data/dataset.csv')

# Label Encoding the categorical variables
header_encoder = LabelEncoder()
para_encoder = LabelEncoder()
format_encoder = LabelEncoder()
interacting_span_encoder = LabelEncoder()
img_encoder = LabelEncoder()
src_img_encoder = LabelEncoder()
red_flag_encoder = LabelEncoder()
table_encoder = LabelEncoder()
sup_encoder = LabelEncoder()
sup_child_encoder = LabelEncoder()
elem_encoder = LabelEncoder()
red_flag_id_encoder = LabelEncoder()

#Transforming the dataset.
dataset['tag_header'] = header_encoder.fit_transform(dataset['tag_header'].values)
dataset['tag_para'] = para_encoder.fit_transform(dataset['tag_para'].values)
dataset['tag_formatting'] = format_encoder.fit_transform(dataset['tag_formatting'].values)
dataset['interacting_span_tag'] = interacting_span_encoder.fit_transform(dataset['interacting_span_tag'].values)
dataset['tag_img'] = img_encoder.fit_transform(dataset['tag_img'].values)
dataset['src_img_interaction'] = src_img_encoder.fit_transform(dataset['src_img_interaction'].values)
dataset['red_flag_class'] = red_flag_encoder.fit_transform(dataset['red_flag_class'].values)
dataset['tag_table'] = table_encoder.fit_transform(dataset['tag_table'].values)
dataset['tag_sup'] = sup_encoder.fit_transform(dataset['tag_sup'].values)
dataset['tag_sup_child'] = sup_child_encoder.fit_transform(dataset['tag_sup_child'].values)
dataset['tag_elem'] = elem_encoder.fit_transform(dataset['tag_elem'].values)
dataset['red_flag_id'] = red_flag_id_encoder.fit_transform(dataset['red_flag_id'].values)

dataset['height_width_diff'] = np.cbrt(dataset['height_width_diff'].values)

#Transforming the variables
data = dataset.iloc[:, :-2]
data['tag_header_y_interacted'] = np.multiply(data['tag_header'], data['relative_y_coord'])
data['span_interaction_y_interacted'] = np.multiply(data['interacting_span_tag'], data['relative_y_coord'])
data['tag_para_y_interacted'] = np.multiply(data['tag_para'], data['relative_y_coord'])
data = data.drop(['tag_dl_type', 'tag_math_type', 'tag_math_elem', 'tag_annotation'], axis = 1)

y = data['label'].values
data = data.drop(['label'], axis = 1)
X = data.iloc[:,:].values

model = RFC(X, y)
pickle.dump(model, open("second_classifier.pkl", "wb"))
encoders = (header_encoder, para_encoder, format_encoder, interacting_span_encoder, img_encoder
            , src_img_encoder, red_flag_encoder, table_encoder, sup_encoder, sup_child_encoder,
            elem_encoder, red_flag_id_encoder)
pickle.dump(encoders, open("second_phase_encoders.pkl", "wb"))