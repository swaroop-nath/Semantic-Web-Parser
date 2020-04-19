from sklearn.preprocessing import StandardScaler

class CustomScaler:
    def __init__(self):
        self.scaler = StandardScaler()
    
    def fit(self, X, y):
        self.scaler = self.scaler.fit(X)
        return self
    
    def transform(self, X):
        X = self.scaler.transform(X)
        return X