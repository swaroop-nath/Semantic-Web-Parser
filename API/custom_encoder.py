from sklearn.preprocessing import LabelEncoder

class CustomEncoder:
    def __init__(self,categories):
        self.encoders = []
        self.categories = categories
        
    def fit(self, X, y):
        for category in self.categories:
            self.encoders.append(LabelEncoder())
            self.encoders[-1].fit(X[category])
        return self
            
    def transform(self, X):
        for index, category in enumerate(self.categories):
            X[category] = self.encoders[index].transform(X[category])
            
        return X