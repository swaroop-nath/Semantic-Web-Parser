import itertools
import re, os
from selenium import webdriver
import numpy as np
import pickle
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

header_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
formatting_tags = ['i', 'b', 'u', 'em', 'small', 'strike', 'strong'] 
class_values = ['thumb', 'image', 'caption', 'toc', 'infobox', 'img', 'reflist', 'nowrap', 'reference', 'navbox', 'footer', 'catlinks']
math_element_tags = ['mi', 'mo', 'mrow', 'mstyle', 'mfrac', 'msub', 'mtable', 'mtr', 'mtd', 'mn', 'mover', 'munder', 'msqrt', 'msup', 'mtext']
table_tag_values = ['table', 'tbody']
td_type_values = ['td', 'tr', 'th']
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
    if name == 'a': return FLAG_A
    if name == 'td' or name == 'tr' or name == 'th': return FLAG_TABLE_ELEMENT
    
def  find_class_type(class_value):
    class_value = ''.join(class_value)
    for value in class_values:
        if value in class_value: 
            return FLAG_UNNECESSARY_CLASS 
    if 'head' in class_value: 
        return FLAG_SPAN_INTERACTION

def find_id_type(id):
    id = id.lower()
    if id == 'references' or 'external' in id: return FLAG_UNNECESSARY_ID
    
# This method returns the feature vector for each element
def extract_features(element_soup, driver, root_width, root_height):
    feature_list = {'tag_header': None, 'tag_para': None,'tag_formatting': None, 
                    'word_count': None, 'interacting_span_tag': None, 'relative_x_coord': None,
                    'relative_y_coord': None, 'relative_listings': None, 'relative_hyperlinks': None,
                    'tag_img': None, 'src_img_interaction': None, 'red_flag_class': None,
                    'tag_table': None, 'tag_sup': None, 'tag_sup_child': None,
                    'tag_elem': None, 'red_flag_id': None, 'relative_table_elements': None,
                    'height_width_diff': None, 'tag_header_y_interacted': None,
                    'span_interaction_y_interacted': None, 'tag_para_y_interacted': None}
    
    tag_appends = {'h': 'NO', 'p': 'NO', 'f': 'NO', 's': 'NO', 'i': 'NO', 't': 'NO', 
                   'sup': 'NO', 'sup_child': 'NO', 'tab_elem': 'NO'}
    FLAG_VALUE = find_tag_type(element_soup.name)
    if FLAG_VALUE is FLAG_HEADER: tag_appends['h'] = 'YES'
    elif FLAG_VALUE is FLAG_PARA: tag_appends['p'] = 'YES'
    elif FLAG_VALUE is FLAG_FORMATTING: tag_appends['f'] = 'YES'
    elif FLAG_VALUE is FLAG_SPAN: tag_appends['s'] = 'YES'
    elif FLAG_VALUE is FLAG_IMG: tag_appends['i'] = 'YES'
    elif FLAG_VALUE is FLAG_TABLE: tag_appends['t'] = 'YES'
    elif FLAG_VALUE is FLAG_SUP: tag_appends['sup'] = 'YES'
    elif FLAG_VALUE is FLAG_A:
        parent = element_soup.parent
        if parent.name == 'sup': tag_appends['sup_child'] = 'YES'
    elif FLAG_VALUE is FLAG_TABLE_ELEMENT: tag_appends['tab_elem'] = 'YES'

    feature_list['tag_header'] = tag_appends['h']
    feature_list['tag_para'] = tag_appends['p']
    feature_list['tag_formatting'] = tag_appends['f']
    feature_list['tag_img'] = tag_appends['i']
    feature_list['tag_table'] = tag_appends['t']
    feature_list['tag_sup'] = tag_appends['sup']
    feature_list['tag_sup_child'] = tag_appends['sup_child']
    feature_list['tag_elem'] = tag_appends['tab_elem']
    
    text = element_soup.text.strip()
    num_words = len(re.split(regexp, text))
    if len(text) == 0: 
        feature_list['word_count'] = 0
        num_words = 0
    else: feature_list['word_count'] = num_words
    
    class_appends = {'r': 'NO', 's': 'NO'}
    if 'class' in element_soup.attrs:
        FLAG_CLASS_VALUE = find_class_type(element_soup.attrs['class'])
        if FLAG_CLASS_VALUE is FLAG_UNNECESSARY_CLASS: class_appends['r'] = 'YES'
        elif FLAG_CLASS_VALUE is FLAG_SPAN_INTERACTION and tag_appends['s'] is 'YES': class_appends['s'] = 'YES'

    feature_list['red_flag_class'] = class_appends['r']
    feature_list['interacting_span_tag'] = class_appends['s']

    id_append = {'i': 'NO'}
    if 'id' in element_soup.attrs:
        FLAG_ID_VALUE = find_id_type(element_soup.attrs['id'])
        if FLAG_ID_VALUE is FLAG_UNNECESSARY_ID: id_append['i'] = 'YES'
            
    feature_list['red_flag_id'] = id_append['i']
    
    num_li_ol = len(element_soup.find_all('li'))
    if num_words != 0: feature_list['relative_listings'] = num_li_ol/(num_words)
    else: feature_list['relative_listings'] = 10 # How to remove this nan?

    num_hyperlinks = len(element_soup.find_all(lambda tg: tg.name == "a" and len(tg.attrs) > 1 and 'href' in tg.attrs))
    if num_words != 0: feature_list['relative_hyperlinks'] = num_hyperlinks/(num_words)
    else: feature_list['relative_hyperlinks'] = 10 # How to remove this nan?

    if tag_appends['i'] is 'YES' and 'src' in element_soup.attrs: feature_list['src_img_interaction'] = 'YES'
    else: feature_list['src_img_interaction'] = 'NO'

    num_td_tr_th = len(element_soup.find_all('td')) + len(element_soup.find_all('tr')) + len(element_soup.find_all('th'))
    if num_words != 0: feature_list['relative_table_elements'] = num_td_tr_th/(num_words)
    else: feature_list['relative_table_elements'] = 100 # How to remove this nan?
    
    try:
        x_path_tag = xpath_soup(element_soup)
        element = driver.find_element_by_xpath(x_path_tag)
        feature_list['relative_x_coord'] = element.location.get('x')/root_width
        feature_list['relative_y_coord'] = element.location.get('y')/root_height
        temp_h = element.size.get('height')
        temp_w = element.size.get('width')
        temp_h = 0 if temp_h is None else temp_h
        temp_w = 0 if temp_w is None else temp_w
        feature_list['height_width_diff'] = temp_h - temp_w
    except NSEE:
        feature_list['relative_x_coord'] = 0 # How to remove this nan?
        feature_list['relative_y_coord'] = 0 # How to remove this nan?
        feature_list['height_width_diff'] = 0 # How to remove this nan?
        
    return feature_list
    
# This method is the one which traverses all the nodes
# in the tree and removes uncessary nodes(along with their children).
def filter_element(features):
    model_filename = r'second_phase/second_classifier.pkl'
    encoders_filename = r'second_phase/second_phase_encoders.pkl'
    
    model = pickle.load(open(model_filename, 'rb'))
    (header_encoder, para_encoder, format_encoder, interacting_span_encoder, img_encoder
            , src_img_encoder, red_flag_encoder, table_encoder, sup_encoder, sup_child_encoder,
            elem_encoder, red_flag_id_encoder) = pickle.load(open(encoders_filename, 'rb'))
    
    features['tag_header'] = header_encoder.transform([features['tag_header']])[0]
    features['tag_para'] = para_encoder.transform([features['tag_para']])[0]
    features['tag_formatting'] = format_encoder.transform([features['tag_formatting']])[0]
    features['interacting_span_tag'] = interacting_span_encoder.transform([features['interacting_span_tag']])[0]
    features['tag_img'] = img_encoder.fit_transform([features['tag_img']])[0]
    features['src_img_interaction'] = src_img_encoder.transform([features['src_img_interaction']])[0]
    features['red_flag_class'] = red_flag_encoder.transform([features['red_flag_class']])[0]
    features['tag_table'] = table_encoder.transform([features['tag_table']])[0]
    features['tag_sup'] = sup_encoder.transform([features['tag_sup']])[0]
    features['tag_sup_child'] = sup_child_encoder.transform([features['tag_sup_child']])[0]
    features['tag_elem'] = elem_encoder.transform([features['tag_elem']])[0]
    features['red_flag_id'] = red_flag_id_encoder.transform([features['red_flag_id']])[0]
    
    features['height_width_diff'] = np.cbrt(features['height_width_diff'])
    
    features['tag_header_y_interacted'] = np.multiply(features['tag_header'], features['relative_y_coord'])
    features['span_interaction_y_interacted'] = np.multiply(features['interacting_span_tag'], features['relative_y_coord'])
    features['tag_para_y_interacted'] = np.multiply(features['tag_para'], features['relative_y_coord'])
    
    X = np.fromiter(features.values(), float)
    label = model.predictValues(X.reshape(1,-1))[0]
    
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