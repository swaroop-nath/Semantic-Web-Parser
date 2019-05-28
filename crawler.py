import data_gathering_script as gatherer

for i in range(32, 41):
    if i not in [33,38]:
        f = open('List of Sites\site_' + str(i) + '.html', 'r', encoding = 'utf8', errors = 'ignore')
        URI = 'file:///D:/Passion/Machine%20Learning/Projects/Semantic_Web_Parser/List%20of%20Sites/site_'+ str(i) +'.html'
        content = f.read()
        gatherer.extractFrom(content, URI)