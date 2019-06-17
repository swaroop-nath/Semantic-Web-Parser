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
X[:, 3] = LabelEncoder().fit_transform(X[:, 3])
X[:, 7] = LabelEncoder().fit_transform(X[:, 7])
X[:, 8]= LabelEncoder().fit_transform(X[:, 8])

# Training the model on the entire dataset
model = rfc(X, y)
pickle.dump(model, open("first_classifier.pkl", "wb"))