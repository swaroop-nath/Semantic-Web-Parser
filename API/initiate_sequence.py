from bs4 import BeautifulSoup, NavigableString
from selenium import webdriver
import pickle
import validators
import itertools
from TreeStructure import Node
import urllib.request as request
import re

accepted_content_classifiers = ['content', 'primary', 'body', 'main', 'contain']
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

def extractFeatures(child_soup, root_area, driver):
    if not isinstance(child_soup, NavigableString):
        feature_list  = {'tag_h': None, 'tag_p': None, 'tag_formatting': None, 'tag_table': None, 'word_count': None, 'children_ratio': None,
                            'id_relevance_extent': None, 'tag_main': None, 'tag_article': None, 'x': None, 'y': None , 
                            'height': None, 'width': None, 'element_area_ratio': None}
        
        feature_list['tag_h'] = len(child_soup.find_all('h1')) + len(child_soup.find_all('h2')) + len(child_soup.find_all('h3')) + len(child_soup.find_all('h4')) + len(child_soup.find_all('h5')) + len(child_soup.find_all('h6'))
        feature_list['tag_p'] = len(child_soup.find_all('p'))
        feature_list['tag_formatting'] = len(child_soup.find_all('b')) + len(child_soup.find_all('i')) + len(child_soup.find_all('u')) + len(child_soup.find_all('em')) + len(child_soup.find_all('small')) + len(child_soup.find_all('strike')) + len(child_soup.find_all('li')) + len(child_soup.find_all('ul')) + len(child_soup.find_all('ol'))

        if len(child_soup.find_all('table')) > 0: feature_list['tag_table'] = 'YES'
        else: feature_list['tag_table'] = 'NO'
        
        text_content = child_soup.text.strip()
        word_list = re.split(regexp, text_content)
        feature_list['word_count'] = (len(word_list))
        if len(list(child_soup.children)) != 0: feature_list['children_ratio'] = (len(list(child_soup.children))/(len(text_content)+1))
        else: feature_list['children_ratio'] = 'nan'

        if len(child_soup.find_all('main')) > 0:
                feature_list["tag_main"] = 'YES'
        else: 
            feature_list["tag_main"] = 'NO'
        if len(child_soup.find_all('article')) > 0: 
            feature_list["tag_article"] = 'YES'
        else: 
            feature_list["tag_article"] = 'NO'

        id_class_role = [child_soup.get('id'), child_soup.get('class'), child_soup.get('role')]
        feature_list['id_relevance_extent'] = findRelevanceExtent(id_class_role)

        x_path_child = xpath_soup(child_soup)
        element = driver.find_element_by_xpath(x_path_child)
        feature_list['x'] = element.location.get('x')
        feature_list['y'] = element.location.get('y')
        temp_h = element.size.get('height')
        temp_w = element.size.get('width')
        if temp_h is None: feature_list['height'] = 'nan'
        else: feature_list['height'] = temp_h
        if temp_w is None: feature_list['width'] = 'nan'
        else: feature_list['width'] = temp_w
        if temp_h is None or temp_w is None: feature_list['element_area_ratio'] = 0
        else: feature_list['element_area_ratio'] = temp_h*temp_w/root_area

        return feature_list
    else:
        return None

def summarizeFrom(url):
    if not validators.url(url):
        raise Exception('Input URL is malformed.')
    
    content = request.urlopen(url)
    root_soup = BeautifulSoup(content, 'lxml')
    children_soup = list(filter(lambda a: a != '\n', root_soup.body.children))

    driver = webdriver.Firefox()
    driver.get(url)

    root_x_path = xpath_soup(root_soup.html)
    root_element = driver.find_element_by_xpath(root_x_path)
    root_area = root_element.size.get('width') * root_element.size.get('height')

    dom_tree_root = Node(soup = root_soup.body)
    for child in children_soup:
        extracted_features = extractFeatures(child, root_area, driver) # This is supposed to be a dictionary
        child_node = None
        if extracted_features is None:
            child_node = Node(soup = child, token = 0)
        else:
            child_node = Node(soup = child, features= extracted_features)
        dom_tree_root.addChild(child_node)
    
    # Next step - call first classifier and identify Main Content Node. Then, collect data for children of that node
