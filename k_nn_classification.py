from sklearn.neighbors import KNeighborsClassifier as KNNClassifier


class KNN:
    classifier = None
    def __init__(self,X_train, y_train):
        self.classifier = KNNClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
        self.classifier.fit(X_train, y_train)
    
    def predictValues(self,X_test):
        if self.classifier is None: raise Exception('ERR: Called on a NoneType Classifier\nCall initClassifier() prior to predicting values')
        return self.classifier.predict(X_test)