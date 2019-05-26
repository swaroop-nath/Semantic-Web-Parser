import urllib.request as request
from bs4 import BeautifulSoup
import re
from pandas import DataFrame, ExcelWriter

# A tempporary URL to test the working of the feature extraction algorithm
url = 'https://stackoverflow.com/questions/13336576/extracting-an-information-from-web-page-by-machine-learning'

accepted_content_classifiers = ['content', 'primary', 'body', 'main']
tag_h= []
tag_p = []
tag_formatting = []
tag_table = []  #Boolean Value - Possible values: 'Yes' and 'No'
word_count = []
children_ratio = []  #This ratio signifies the sparsity of children tags in the content of an element
id_relevance_extent = []  #Integer Value - Possible Values: 0, 1, 2, 3; this sees if the id/class/role attribute has a value from the accepted words, if it does, then the check is done for how many words from the accepted list match the value
tag_main = []  #Boolean value - Possible Values: 'Yes' and 'No'
tag_article = []  #Boolean value - Possible Values: 'Yes' and 'No'

regexp = '; |, | |\n|-\*'

def findRelevanceExtent(id_class_role):
    relevance_extent = 0
    flag_0 = False
    flag_1 = False
    flag_2 = False
    for i in range(3):
        if not id_class_role[i] is None: ''.join(id_class_role[i])
    for content_classifier in accepted_content_classifiers:
        if not id_class_role[0] is None and content_classifier in id_class_role[0]: flag_0 = True
        if not id_class_role[1] is None and content_classifier in id_class_role[1]: flag_1 = True
        if not id_class_role[2] is None and content_classifier in id_class_role[2]: flag_2 = True
        if flag_0 or flag_1 or flag_2: relevance_extent = relevance_extent + 1
        flag_0 = False
        flag_1 = False
        flag_2 = False
    return relevance_extent

def featureExtraction(soup):
    divs = soup.find_all('div')
    for div in divs:
        tag_h.append(len(div.find_all('h1')) + len(div.find_all('h2')) + len(div.find_all('h3')) + len(div.find_all('h4')) + len(div.find_all('h5')) + len(div.find_all('h6')))
        tag_p.append(len(div.find_all('p')))
        tag_formatting.append(len(div.find_all('b')) + len(div.find_all('i')) + len(div.find_all('u')) + len(div.find_all('em')) + len(div.find_all('small')) + len(div.find_all('strike')) + len(div.find_all('li')) + len(div.find_all('ul')) + len(div.find_all('ol')))
        if len(div.find_all('table')) > 0: tag_table.append('YES')
        else: tag_table.append('NO')
        text_content = div.text.strip()
        word_list = re.split(regexp, text_content)
        word_count.append(len(word_list))
        children_ratio.append(len(list(div.children))/(len(text_content)+1))
        if len(div.find_all('main')) > 0:
            tag_main.append('YES')
        else: 
            tag_main.append('NO')
        if len(div.find_all('article')) > 0: 
            tag_article.append('YES')
        else: 
            tag_article.append('NO')
        id_class_role = [div.get('id'), div.get('class'), div.get('role')]
        id_relevance_extent.append(findRelevanceExtent(id_class_role))

        
def formCSVData():
    data = {'tag_h': tag_h,'tag_p': tag_p,'tag_formatting': tag_formatting,'tag_table': tag_table,'word_count': word_count,'children_ratio': children_ratio,'id_relevance_extent': id_relevance_extent,'tag_main': tag_main,'tag_article': tag_article}
    # col_names = ['tag_h1', 'tag_h2', 'tag_h3', 'tag_h4', 'tag_h5', 'tag_h6', 'tag_p', 'tag_b', 'tag_i', 'tag_u', 'tag_em', 'tag_small', 'tag_strike', 'tag_li', 'tag_ol', 'tag_ul', 'tag_table', 'word_count', 'children_ratio', 'id_relevance_extent', 'tag_main', 'tag_article']
    df = DataFrame(data)
    writer = ExcelWriter('data_gathered.xlsx', engine = 'xlsxwriter')
    df.to_excel(writer, sheet_name = 'Sheet1')
    writer.save()

# markup = request.urlopen(url)
# soup_object = BeautifulSoup(markup, 'lxml')

temp_html_source = open('temp_html_source.txt', 'r', encoding='utf8')
soup_object = BeautifulSoup(temp_html_source.read(), 'lxml')

featureExtraction(soup_object)
formCSVData()