from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.pipeline import Pipeline
from custom_encoder import CustomEncoder
import pickle

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
model = RandomForestClassifier(n_estimators = 20, max_depth = 4)
estimators = [('encoder', CustomEncoder(['tag_header', 'tag_para', 'tag_formatting', 'tag_img', 'interacting_span_tag', 'red_flag_class', 'tag_math_span', 'src_img_interaction', 'tag_table', 'tag_sup', 'tag_unnecessary_header', 'red_flag_id'])), ('rfc', model)]
#
pipeline = Pipeline(steps = estimators).fit(X, y)
with open('second_model.mdl', 'wb') as file:
    pickle.dump(pipeline, file)