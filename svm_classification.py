from sklearn.svm import SVC

class SVClassifier:
    classifier = None
    def __init__(self, X_train, y_train):
        self.classifier = SVC(kernel = 'poly', degree=2)
        self.classifier.fit(X_train, y_train)
    
    def predictValues(self, X_test):
        return self.classifier.predict(X_test)