import data_gathering_script as gatherer

for i in range(1, 41):
    f = open('List of Sites\site_' + str(i) + '.html', 'r', encoding = 'utf8', errors = 'ignore')
    content = f.read()
    gatherer.extractFrom(content)