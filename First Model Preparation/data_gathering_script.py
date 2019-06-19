import urllib.request as request
from bs4 import BeautifulSoup, NavigableString
import re
from pandas import DataFrame, ExcelWriter
from selenium import webdriver
import itertools

# A tempporary URL to test the working of the feature extraction algorithm
url = 'https://stackoverflow.com/questions/13336576/extracting-an-information-from-web-page-by-machine-learning'

accepted_content_classifiers = ['content', 'primary', 'body', 'main', 'contain']
tag_h= []
tag_p = []
tag_formatting = []
tag_table = []  #Boolean Value - Possible values: 'Yes' and 'No'
word_count = []
children_ratio = []  #This ratio signifies the sparsity of children tags in the content of an element
# children = []
id_relevance_extent = []  #Integer Value - Possible Values: 0, 1, 2, 3; this sees if the id/class/role attribute has a value from the accepted words, if it does, then the check is done for how many words from the accepted list match the value
tag_main = []  #Boolean value - Possible Values: 'Yes' and 'No'
tag_article = []  #Boolean value - Possible Values: 'Yes' and 'No'
class_value = []
coord_x = []
coord_y = []
height = []
width = []
element_area_ratio = []

regexp = '; |, | |\n|-\*'

def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

def findRelevanceExtent(id_class_role):
    relevance_extent = 0
    flag_0 = False
    flag_1 = False
    flag_2 = False
    for i in range(3):
        if not id_class_role[i] is None: id_class_role[i] = ''.join(id_class_role[i])
    for content_classifier in accepted_content_classifiers:
        if not id_class_role[0] is None and content_classifier in id_class_role[0]: flag_0 = True
        if not id_class_role[1] is None and content_classifier in id_class_role[1]: flag_1 = True
        if not id_class_role[2] is None and content_classifier in id_class_role[2]: flag_2 = True
        if flag_0 or flag_1 or flag_2: relevance_extent = relevance_extent + 1
        flag_0 = False
        flag_1 = False
        flag_2 = False
    return relevance_extent

def featureExtraction(soup, driver, root_area):
    children_soup = soup.body.children
    children_soup = list(filter(lambda a: a != '\n', children_soup))
    for div in children_soup:
        # print(type(div))
        if not isinstance(div, NavigableString):
            tag_h.append(len(div.find_all('h1')) + len(div.find_all('h2')) + len(div.find_all('h3')) + len(div.find_all('h4')) + len(div.find_all('h5')) + len(div.find_all('h6')))
            tag_p.append(len(div.find_all('p')))
            tag_formatting.append(len(div.find_all('b')) + len(div.find_all('i')) + len(div.find_all('u')) + len(div.find_all('em')) + len(div.find_all('small')) + len(div.find_all('strike')) + len(div.find_all('li')) + len(div.find_all('ul')) + len(div.find_all('ol')))
            if len(div.find_all('table')) > 0: tag_table.append('YES')
            else: tag_table.append('NO')
            text_content = div.text.strip()
            word_list = re.split(regexp, text_content)
            word_count.append(len(word_list))
            if len(list(div.children)) != 0: children_ratio.append(len(list(div.children))/(len(text_content)+1))
            else: children_ratio.append('nan')
            # children.append(len(list(div.children)))
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
            flag_class = False
            for x in id_class_role:
                if not x is None:
                    flag_class = True
                    class_value.append(x)
                    break
            if not flag_class: class_value.append('nan')
            x_path_div = xpath_soup(div)
            element = driver.find_element_by_xpath(x_path_div)
            coord_x.append(element.location.get('x'))
            coord_y.append(element.location.get('y'))
            temp_h = element.size.get('height')
            temp_w = element.size.get('width')
            if temp_h is None: height.append('nan')
            else: height.append(temp_h)
            if temp_w is None: width.append('nan')
            else: width.append(temp_w)
            if temp_h is None or temp_w is None: element_area_ratio.append('0')
            else: element_area_ratio.append(temp_h*temp_w/root_area)

        
def formCSVData(i):
    data = {'tag_h': tag_h,'tag_p': tag_p,'tag_formatting': tag_formatting,'tag_table': tag_table,'word_count': word_count,'children_ratio': children_ratio,'id_relevance_extent': id_relevance_extent,'tag_main': tag_main,'tag_article': tag_article,'x': coord_x,'y': coord_y,'height': height,'width': width,'element_area_ratio': element_area_ratio ,'class_value': class_value}
    # print('tag_h:' + str(len(tag_h)) + ', coord_x: ' + str(len(coord_x)) + ', coord_y: ' + str(len(coord_y)) + ', height: ' + str(len(height)) + ', width: ' + str(len(width)) + ', element_are_ratio: ' + str(len(element_area_ratio)))
    # col_names = ['tag_h1', 'tag_h2', 'tag_h3', 'tag_h4', 'tag_h5', 'tag_h6', 'tag_p', 'tag_b', 'tag_i', 'tag_u', 'tag_em', 'tag_small', 'tag_strike', 'tag_li', 'tag_ol', 'tag_ul', 'tag_table', 'word_count', 'children_ratio', 'id_relevance_extent', 'tag_main', 'tag_article']
    df = DataFrame(data)
    writer = ExcelWriter('Second Iteration Data\data_gathered_part_first_segmentation_'+str(i+2)+'.xlsx', engine = 'openpyxl')
    # writer = ExcelWriter('xyz.xlsx', engine = 'openpyxl')
    df.to_excel(writer, sheet_name = 'Sheet1', header = True)
    writer.save()

def extractFrom(content, URI, i):
    soup_object = BeautifulSoup(content, 'lxml')
    driver = webdriver.Firefox(executable_path=r'D:\Softwares\Anaconda\Anaconda\geckodriver-v0.24.0-win64\geckodriver.exe')
    # print(URI)
    driver.get(URI)
    root_x_path = xpath_soup(soup_object.html)
    root_element = driver.find_element_by_xpath(root_x_path)
    # print(root_element.size)
    root_area = root_element.size.get('width') * root_element.size.get('height')
    # print(root_area)
    # print(type(root_area))
    featureExtraction(soup_object, driver, root_area)
    formCSVData(i)
    driver.quit()
    # root_area = 0
    tag_h.clear()
    tag_p.clear()
    tag_formatting.clear()
    tag_table.clear()
    word_count.clear()
    children_ratio.clear()
    # children.clear()
    id_relevance_extent.clear()
    tag_main.clear()
    tag_article.clear()
    class_value.clear()
    coord_x.clear()
    coord_y.clear()
    height.clear()
    width.clear()
    element_area_ratio.clear()


# Driver Program to test the functions
# markup = request.urlopen(url)
# soup_object = BeautifulSoup(markup, 'lxml')

# temp_html_source = open('temp_html_source.txt', 'r', encoding='utf8')
# soup_object = BeautifulSoup(temp_html_source.read(), 'lxml')

# featureExtraction(soup_object)
# formCSVData().clear()