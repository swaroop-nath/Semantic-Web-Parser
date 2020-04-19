import numpy as np
import pandas as pd
import pickle as pkl
from sklearn.preprocessing import StandardScaler
from custom_scaler import CustomScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Importing the dataset
dataset = pd.read_csv(r'Data/dataset.csv')

# Feature Engineering
dataset['Interaction'] = dataset.apply(lambda row: row['Fraction p Children'] + row['Num Words'], axis = 1)

X = dataset.loc[:, ['Fraction p Children', 'Interaction']].values
y = dataset.loc[:, 'Label'].values

# Creating the pipeline
model = LogisticRegression()
steps = [('scaler', CustomScaler()), ('model', model)]
pipeline = Pipeline(steps=steps).fit(X, y)

with open('first_model.mdl', 'wb') as file:
    pkl.dump(pipeline, file)
