import pandas as pd
import numpy as np
from random_forest_classification import RFClassifier as rfc
import pickle
from sklearn.preprocessing import LabelEncoder

# Load the training data
dataset = pd.read_csv("First Classification Data\\final_version_data.csv")
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# Clean the dataset
table_encoder = LabelEncoder()
main_encoder = LabelEncoder()
article_encoder = LabelEncoder()
X[:, 3] = table_encoder.fit_transform(X[:, 3])
X[:, 7] = main_encoder.fit_transform(X[:, 7])
X[:, 8]= article_encoder.fit_transform(X[:, 8])

# Training the model on the entire dataset
model = rfc(X, y)
pickle.dump(model, open("first_classifier.pkl", "wb"))
pickle.dump((table_encoder, main_encoder, article_encoder), open('first_phase_encoders.pkl', 'wb'))