class Node:
    features = {}
    label = float('nan')
    soup_element = None

    children_count = 0
    children = []

    def __init__(self, soup, features = None):
        if features is None:
            self.label = 1
        self.features = features
        self.soup_element = soup

    def addChild(self, child):
        self.children_count += 1
        self.children.append(child)

    def setLabel(self, label):
        self.label = label
    
    def getChildren(self):
        if self.children_count == 0: return -1
        else: return self.children

    def getSoupObject(self):
        return self.soup_element

