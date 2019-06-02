from sklearn.neighbors import KNeighborsClassifier as KNNC

class KNNClassifier:
    classifier = None
    def __init__(self,X_train, y_train):
        self.classifier = KNNC(n_neighbors = 5, metric = 'minkowski', p = 2)
        self.classifier.fit(X_train, y_train)
    
    def predictValues(self,X_test):
        return self.classifier.predict(X_test)