from sklearn.tree import DecisionTreeClassifier

class DTClassifier:
    classifier = None
    def __init__(self, X_train, y_train):
        self.classifier = DecisionTreeClassifier(criterion = 'entropy')
        self.classifier.fit(X_train, y_train)
    
    def predictValues(self, X_test):
        return self.classifier.predict(X_test)