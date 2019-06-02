from sklearn.ensemble import RandomForestClassifier

class RFClassifier:
    classifier = None
    def __init__(self, X_train, y_train):
        self.classifier = RandomForestClassifier(criterion = 'entropy')
        self.classifier.fit(X_train, y_train)
        
    def predictValues(self, X_test):
        return self.classifier.predict(X_test)