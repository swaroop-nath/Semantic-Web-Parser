import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import pickle
from custom_encoder import CustomEncoder

# Load the training data
dataset = pd.read_csv(r"First Classification Data/final_version_data.csv")
X = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1]

model = RandomForestClassifier(n_estimators = 200, max_depth = 4)
estimators = [('encoders', CustomEncoder(['tag_table', 'tag_main', 'tag_article'])), ('model', model)]
pipeline = Pipeline(steps = estimators).fit(X, y)

with open('first_model.mdl', 'wb') as file:
    pickle.dump(pipeline, file)