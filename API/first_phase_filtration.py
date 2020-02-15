from bs4 import BeautifulSoup, NavigableString
import pickle
import itertools
from tree_structure import Node
import re, os
from selenium import webdriver
import numpy as np

MAIN_CONTENT_LABEL = 2

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

def find_relevance_extent(id_class_role):
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

def extract_features(child_soup, root_area, driver):
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
        else: feature_list['children_ratio'] = 1 # nan replacement = 1

        if len(child_soup.find_all('main')) > 0:
                feature_list["tag_main"] = 'YES'
        else: 
            feature_list["tag_main"] = 'NO'
        if len(child_soup.find_all('article')) > 0: 
            feature_list["tag_article"] = 'YES'
        else: 
            feature_list["tag_article"] = 'NO'

        id_class_role = [child_soup.get('id'), child_soup.get('class'), child_soup.get('role')]
        feature_list['id_relevance_extent'] = find_relevance_extent(id_class_role)

        x_path_child = xpath_soup(child_soup)
        element = driver.find_element_by_xpath(x_path_child)
        feature_list['x'] = element.location.get('x')
        feature_list['y'] = element.location.get('y')
        temp_h = element.size.get('height')
        temp_w = element.size.get('width')
        if temp_h is None: feature_list['height'] = 0 # nan replacement = 0
        else: feature_list['height'] = temp_h
        if temp_w is None: feature_list['width'] = 0 # nan replacement = 0
        else: feature_list['width'] = temp_w
        if temp_h is None or temp_w is None: feature_list['element_area_ratio'] = 0
        else: feature_list['element_area_ratio'] = temp_h*temp_w/root_area

        return feature_list
    else:
        return None

def get_main_content(root_node):
    children_nodes = root_node.getChildren()
    model_filename = r'first_phase/first_classifier.pkl'
    encoder_filename = r'first_phase/first_phase_encoders.pkl'
    if children_nodes != -1:
        model = pickle.load(open(model_filename, 'rb'))
        table_encoder, main_encoder, article_encoder = pickle.load(open(encoder_filename, 'rb'))
        for child in children_nodes:
            features = child.features
            print(features)
            print()
            features['tag_table'] = table_encoder.transform([features['tag_table']])[0]
            features['tag_main'] = main_encoder.transform([features['tag_main']])[0]
            features['tag_article'] = article_encoder.transform([features['tag_article']])[0]
            X = np.fromiter(features.values(), float)
            pred = model.predictValues(X.reshape(1,-1))
            child.setLabel(pred[0])
        for child in children_nodes:
            if child.label == MAIN_CONTENT_LABEL: return child
    return None

def do_extrinsic_filtration(content, url):
    chrome_driver_path = r'/Softwares/Web-Drivers/chromedriver'
    os.environ["webdriver.chrome.driver"] = chrome_driver_path
    driver = webdriver.Chrome(chrome_driver_path)
    
    driver.get(url)
    
    root_soup = BeautifulSoup(content, 'lxml')
    children_soup = list(filter(lambda a: a != '\n', root_soup.body.children))

    root_x_path = xpath_soup(root_soup.html)
    root_element = driver.find_element_by_xpath(root_x_path)
    root_area = root_element.size.get('width') * root_element.size.get('height')

    dom_tree_root = Node(soup = root_soup.body)
    for child in children_soup:
        extracted_features = extract_features(child, root_area, driver)
        child_node = None
        if not extracted_features is None:
            child_node = Node(soup = child, features= extracted_features)
        dom_tree_root.addChild(child_node)
    
    
    main_content_node = get_main_content(dom_tree_root)

    driver.close()
    driver.quit()

    return main_content_node


#url = 'https://en.wikipedia.org/wiki/Isaac_Newton'
#node = summarizeFrom(url)
#
#with open('body.txt', 'w') as file:
#    file.write(str(node.getSoupObject()))