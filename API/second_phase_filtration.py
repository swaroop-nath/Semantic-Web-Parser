import itertools
import re, os
from selenium import webdriver
import numpy as np
import pickle
import pandas as pd
from selenium.common.exceptions import NoSuchElementException as NSEE

LABEL_NECESSARY = 1

FLAG_HEADER = 'header'
FLAG_PARA = 'paragraph'
FLAG_FORMATTING = 'formatting'
FLAG_SPAN = 'span'
FLAG_IMG = 'img'
FLAG_TABLE = 'table'
FLAG_SUP = 'sup'
FLAG_A = 'a'
FLAG_TABLE_ELEMENT = 'table_element'
FLAG_UNNECESSARY_ID = 'unnecessary_id'
FLAG_UNNECESSARY_CLASS = 'unnecessary_classes'
FLAG_SPAN_INTERACTION = 'span_interaction'
FLAG_MATH_SPAN = 'math_span'

header_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
formatting_tags = ['i', 'b', 'u', 'em', 'small', 'strike', 'strong', 'pre'] 
class_values = ['thumb', 'image', 'caption', 'toc', 'infobox', 'img', 'reflist', 'nowrap', 'reference', 'navbox', 'footer', 'catlinks', 'hatnote', 'noprint', 'quote', 'empty', 'editsection']
math_element_tags = ['mi', 'mo', 'mrow', 'mstyle', 'mfrac', 'msub', 'mtable', 'mtr', 'mtd', 'mn', 'mover', 'munder', 'msqrt', 'msup', 'mtext']
table_tag_values = ['table', 'tbody']
td_type_values = ['td', 'tr', 'th']
red_flag_texts = ['references', 'see also', 'further reading', 'external links']
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
    
def find_tag_type(name):
    name = name.strip()
    for header in header_tags:
        if header == name: return FLAG_HEADER
    if name == 'span': return FLAG_SPAN
    if name == 'p': return FLAG_PARA 
    for format_tag in formatting_tags:
        if name == format_tag: return FLAG_FORMATTING
    if name == 'img': return FLAG_IMG 
    if 'table' == name or 'tbody' == name: return FLAG_TABLE 
    if name == 'sup': return FLAG_SUP
    
def  find_class_type(class_value):
    class_value = ''.join(class_value)
    for value in class_values:
        if value in class_value: 
            return FLAG_UNNECESSARY_CLASS 
    if 'math' in class_value:
        return FLAG_MATH_SPAN
    if 'head' in class_value: 
        return FLAG_SPAN_INTERACTION

def find_id_type(id):
    id = id.lower()
    if id == 'references' or 'external' in id: return FLAG_UNNECESSARY_ID
    
def is_unnecessary_text(text):
    for val in red_flag_texts:
        if val in text.lower(): return True
    return False
    
# This method returns the feature vector for each element
def extract_features(element_soup, driver, root_width, root_height):
    feature_list = {'tag_header': None, 'tag_para': None, 'tag_formatting': None, 
                    'word_count': None, 'interacting_span_tag': None, 
                    'relative_x_coord': None, 'relative_y_coord': None, 
                    'relative_listings': None, 
                    'relative_hyperlinks': None, 'tag_img': None, 
                    'tag_math_span': None, 'src_img_interaction': None,
                    'red_flag_class': None, 'tag_table': None, 
                    'tag_sup': None, 'tag_unnecessary_header': None, 
                    'red_flag_id': None, 
                    'relative_table_elements': None, 'height': None, 'aspect_ratio': None}
    
    tag_appends = {'h': 'NO', 'p': 'NO', 'f': 'NO', 's': 'NO', 'i': 'NO', 't': 'NO', 
                   'sup': 'NO'}
    FLAG_VALUE = find_tag_type(element_soup.name)
    if FLAG_VALUE is FLAG_HEADER: tag_appends['h'] = 'YES'
    elif FLAG_VALUE is FLAG_PARA: tag_appends['p'] = 'YES'
    elif FLAG_VALUE is FLAG_FORMATTING: tag_appends['f'] = 'YES'
    elif FLAG_VALUE is FLAG_SPAN: tag_appends['s'] = 'YES'
    elif FLAG_VALUE is FLAG_IMG: tag_appends['i'] = 'YES'
    elif FLAG_VALUE is FLAG_TABLE: tag_appends['t'] = 'YES'
    elif FLAG_VALUE is FLAG_SUP: tag_appends['sup'] = 'YES'

    feature_list['tag_header'] = tag_appends['h']
    feature_list['tag_para'] = tag_appends['p']
    feature_list['tag_formatting'] = tag_appends['f']
    feature_list['tag_img'] = tag_appends['i']
    feature_list['tag_table'] = tag_appends['t']
    feature_list['tag_sup'] = tag_appends['sup']
    
    text = element_soup.text.strip()
    
    feature_list['tag_unnecessary_header'] = 'NO'
    
    if FLAG_VALUE is FLAG_HEADER and is_unnecessary_text(text): feature_list['tag_unnecessary_header'] = 'YES'
    
    num_words = len(re.split(regexp, text))
    if len(text) == 0: 
        feature_list['word_count'] = 0
        num_words = 0
    else: feature_list['word_count'] = num_words
    
    class_appends = {'r': 'NO', 's': 'NO', 'm': 'NO'}
    if 'class' in element_soup.attrs:
        FLAG_CLASS_VALUE = find_class_type(element_soup.attrs['class'])
        if FLAG_CLASS_VALUE is FLAG_UNNECESSARY_CLASS: class_appends['r'] = 'YES'
        elif FLAG_CLASS_VALUE is FLAG_SPAN_INTERACTION and tag_appends['s'] is 'YES': class_appends['s'] = 'YES'
        elif FLAG_CLASS_VALUE is FLAG_MATH_SPAN and tag_appends['s'] is 'YES': class_appends['m'] = 'YES'

    feature_list['red_flag_class'] = class_appends['r']
    feature_list['interacting_span_tag'] = class_appends['s']
    feature_list['tag_math_span'] = class_appends['m']

    id_append = {'i': 'NO'}
#    if 'id' in element_soup.attrs:
#        FLAG_ID_VALUE = find_id_type(element_soup.attrs['id'])
#        if FLAG_ID_VALUE is FLAG_UNNECESSARY_ID: id_append['i'] = 'YES'
            
    feature_list['red_flag_id'] = id_append['i']
    
    li_tags = element_soup.find_all('li')
    num_li_tags = len(li_tags)
    num_tags = len(element_soup.findAll())
    num_li_child_tags = 0
    for li in li_tags:
        num_li_child_tags += len(li.findAll())
    num_li_level_tags = num_tags - num_li_child_tags if num_tags > num_li_child_tags else num_tags

    if num_li_level_tags != 0: feature_list['relative_listings'] = num_li_tags/(num_li_level_tags)
    else: feature_list['relative_listings'] = 0
    
    num_hyperlinks = len(element_soup.find_all(lambda tg: tg.name == "a" and len(tg.attrs) > 1 and 'href' in tg.attrs))
    if num_words != 0: feature_list['relative_hyperlinks'] = num_hyperlinks/(num_words)
    else: feature_list['relative_hyperlinks'] = 10 # How to remove this nan?

    if tag_appends['i'] is 'YES' and 'src' in element_soup.attrs: feature_list['src_img_interaction'] = 'YES'
    else: feature_list['src_img_interaction'] = 'NO'

    td_tr_th_tags = element_soup.find_all('td')
    num_td_tr_th = len(td_tr_th_tags)
    num_tags = len(element_soup.findAll())
    num_td_tr_child_tags = 0
    for td_tr_child_tag in td_tr_th_tags:
        num_td_tr_child_tags += len(td_tr_child_tag.findAll())
            
    num_td_tr_level_tags = num_tags - num_td_tr_child_tags if num_tags > num_td_tr_child_tags else num_tags

    if num_td_tr_level_tags != 0: feature_list['relative_table_elements'] = num_td_tr_th/(num_td_tr_level_tags)
    else: feature_list['relative_table_elements'] = 0

    try:
        x_path_tag = xpath_soup(element_soup)
        element = driver.find_element_by_xpath(x_path_tag)
        feature_list['relative_x_coord'] = element.location.get('x')/root_width
        feature_list['relative_y_coord'] = element.location.get('y')/root_height
        temp_h = element.size.get('height')
        temp_w = element.size.get('width')
        temp_h = 0 if temp_h is None else temp_h
        temp_w = 0 if temp_w is None else temp_w
        feature_list['height'] = temp_h
        feature_list['aspect_ratio'] = temp_w/temp_h if temp_h > 0 else 0
    except NSEE:
        feature_list['relative_x_coord'] = 0 # How to remove this nan?
        feature_list['relative_y_coord'] = 0 # How to remove this nan?
        feature_list['height'] = 0
        feature_list['aspect_ratio'] = 0
        
    return feature_list
    
# This method is the one which traverses all the nodes
# in the tree and removes uncessary nodes(along with their children).
def filter_element(features):
    pipeline_file = r'second_phase/second_model.mdl'
    
    model = pickle.load(open(pipeline_file, 'rb'))
    
    X = pd.DataFrame(features, index = [0]) 
    label = model.predict(X)
    
    return label

# This method is the entry point for doing the second-phase-filtration.
def do_intrinsic_filtration(root_node, url):
    chrome_driver_path = r'/Softwares/Web-Drivers/chromedriver'
    os.environ["webdriver.chrome.driver"] = chrome_driver_path
    driver = webdriver.Chrome(chrome_driver_path)
    
    driver.get(url)
    
    root_soup = root_node.getSoupObject()
    
    root_x_path = xpath_soup(root_soup)
    root_element = driver.find_element_by_xpath(root_x_path)
    root_width = root_element.size.get('width')
    root_height = root_element.size.get('height')
    
    elem_queue = []
    
    # Bug - Necessary div is labelled wrongly - ML algo faulty
    
    for child in root_soup.children:
        if child.name is not None:
            features = extract_features(child, driver, root_width, root_height)
            label = filter_element(features)
            if label != LABEL_NECESSARY:
                child.decompose()
            else: 
                elem_queue.append(child)
                
    while (len(elem_queue) > 0):
        element = elem_queue.pop(0)
        for child in element.children:
            if child.name is not None:
                features = extract_features(child, driver, root_width, root_height)
                label = filter_element(features)
                if label != LABEL_NECESSARY:
                    child.decompose()
                else: 
                    elem_queue.append(child)
    
    driver.close()
    driver.quit()

    return root_soup