import data_gathering_script as gatherer

for i in range(70, 76):
    if i not in []:
        f = open('List of Sites\site_' + str(i) + '.html', 'r', encoding = 'utf8', errors = 'ignore')
        URI = 'file:///D:/Passion/Machine%20Learning/Projects/Semantic_Web_Parser_Model_Builder/List%20of%20Sites/site_'+ str(i) +'.html'
        content = f.read()
        gatherer.extractFrom(content, URI, i)

