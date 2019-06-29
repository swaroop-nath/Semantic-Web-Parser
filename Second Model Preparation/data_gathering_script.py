import urllib.request as request
from bs4 import BeautifulSoup, NavigableString
import re
from pandas import DataFrame, ExcelWriter
from selenium import webdriver
import itertools
import time
from selenium.common.exceptions import NoSuchElementException as NSEE

header_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
formatting_tags = ['i', 'b', 'u', 'em', 'small', 'strike', 'strong']
listing_tags = ['li', 'ol']
class_values = ['thumb', 'image', 'caption', 'toc', 'infobox', 'img']
table_tag_values = ['table', 'tbody']
td_type_values = ['td', 'tr', 'th']
regexp = '; |, | |\n|-\*'

tag_header = [] # This indicates if the tag has any header tags (h1, h2, h3, h4, h5, h6) --| --
tag_p = [] # This indicates if the tag is a paragraph tag (p) -| --
tag_formatting = [] # This indicatesif the current tag is a formatting tag (b, i, u, em, strong, small, strike) --| -- 
word_count = [] # This indicates the number of words contained within the tag -| --
tag_span_interaction = [] # This feature defines the interaction between variables - is tag span? and does class value have 'head'? -| --
relative_x = [] # This is the x value of the element standardized by the width of the page -| --
relative_y = [] # This is the y value of the element standardized by the height of the page -| --
number_listing_per_word = []  # This is the number of li/ol children tags divided by the number of words contained by the tag --| --
number_hyper_per_word = [] # This is the number of hyperlinks (a tags with href attributes) inside the tag divided by the number of words contained by the tag -| --
tag_img = [] # This indicates if the current tag is an img tag -| --
attr_src_interation = [] # This is a interaction term between the variables - does the tag have src attribute and and is the tag img? -| -- 
is_class_value_relevant = [] # This indicates if the class value is one of - (thumb, image, caption, toc, infobox,img) --|--
tag_table = [] # This indicates if the tag is one of - (table, tbody) --| --
number_td_type_per_word = [] # This indicates the number of - (td, tr, th) tags contained with the current tag divided by the number of words --| --
diff_height_width = []
name = []
attrs = []

FLAG_HEADER = 'header'
FLAG_PARA = 'paragraph'
FLAG_FORMATTING = 'formatting'
FLAG_SPAN = 'span'
FLAG_IMG = 'img'
FLAG_TABLE = 'table'
FLAG_UNNECESSARY_CLASS = 'unnecessary_classes'
FLAG_SPAN_INTERACTION = 'span_interaction'

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

def findTagType(name):
    for header in header_tags:
        if header in name: return FLAG_HEADER
    if 'p' in name: return FLAG_PARA
    for format_tag in formatting_tags:
        if format_tag in name: return FLAG_FORMATTING
    if 'span' in name: return FLAG_SPAN
    if 'img' in name: return FLAG_IMG
    if 'table' in name or 'tbody' in name: return FLAG_TABLE

def  findClassType(class_value):
    for value in class_values:
        if value in class_value: return FLAG_UNNECESSARY_CLASS
    if 'head' in class_value: return FLAG_SPAN_INTERACTION

def featureExtraction(soup, driver, root_width, root_height):
    tags = soup[0].find_all()
    for tag in tags:
        if not isinstance(tag, NavigableString):
            tag_appends = {'h': 'NO', 'p': 'NO', 'f': 'NO', 's': 'NO', 'i': 'NO', 't': 'NO'}
            FLAG_VALUE = findTagType(tag.name)
            if FLAG_VALUE is FLAG_HEADER: tag_appends['h'] = 'YES'
            elif FLAG_VALUE is FLAG_PARA: tag_appends['p'] = 'YES'
            elif FLAG_VALUE is FLAG_FORMATTING: tag_appends['f'] = 'YES'
            elif FLAG_VALUE is FLAG_SPAN: tag_appends['s'] = 'YES'
            elif FLAG_VALUE is FLAG_IMG: tag_appends['i'] = 'YES'
            elif FLAG_VALUE is FLAG_TABLE: tag_appends['t'] = 'YES'
            
            tag_header.append(tag_appends['h'])
            tag_p.append(tag_appends['p'])
            tag_formatting.append(tag_appends['f'])
            tag_img.append(tag_appends['i'])
            tag_table.append(tag_appends['t'])

            text = tag.text.strip()
            num_words = len(re.split(regexp, text))
            word_count.append(num_words)

            class_appends = {'r': 'NO', 's': 'NO'}
            if 'class' in tag.attrs:
                FLAG_CLASS_VALUE = findClassType(tag.attrs['class'])
                if FLAG_CLASS_VALUE is FLAG_UNNECESSARY_CLASS: class_appends['r'] = 'YES'
                elif FLAG_CLASS_VALUE is FLAG_SPAN_INTERACTION and tag_appends['s'] is 'YES': class_appends['s'] = 'YES'

            is_class_value_relevant.append(class_appends['r'])
            tag_span_interaction.append(class_appends['s'])

            num_li_ol = len(tag.find_all('li')) +len(tag.find_all('ol'))
            number_listing_per_word.append(num_li_ol/(num_words + 0.1)) # 0.1 added to avoid division by zero.

            num_hyperlinks = len(tag.find_all(lambda tg: tg.name == "a" and len(tg.attrs) > 1 and 'href' in tg.attrs))
            number_hyper_per_word.append(num_hyperlinks/(num_words+0.1))

            if tag_appends['i'] is 'YES' and 'src' in tag.attrs: attr_src_interation.append('YES')
            else: attr_src_interation.append('NO')

            num_td_tr_th = len(tag.find_all('td')) + len(tag.find_all('tr')) + len(tag.find_all('th'))
            number_td_type_per_word.append(num_td_tr_th/(num_words + 0.1))

            try:
                x_path_tag = xpath_soup(tag)
                element = driver.find_element_by_xpath(x_path_tag)
                relative_x.append(element.location.get('x')/root_width)
                relative_y.append(element.location.get('y')/root_height)
                temp_h = element.size.get('height')
                temp_w = element.size.get('width')
                temp_h = 0 if temp_h is None else temp_h
                temp_w = 0 if temp_w is None else temp_w
                diff_height_width.append(temp_h - temp_w)
            except NSEE:
                relative_x.append('nan')
                relative_y.append('nan')
                diff_height_width.append('nan')

            name.append(tag.name)
            attrs.append(list(tag.attrs.values()))
            FLAG_VALUE = ''

def clearAll():
    pass
        
def formCSVData():
    data = {'tag_header': tag_header, 'tag_para': tag_p, 'tag_formatting': tag_formatting, 'word_count': word_count, 'interacting_span_tag': tag_span_interaction, 'relative_x_coord': relative_x, 'relative_y_coord': relative_y, 'relative_listings': number_listing_per_word, 'relative_hyperlinks': number_hyper_per_word, 'tag_img': tag_img, 'src_img_interaction': attr_src_interation, 'red_flag_class': is_class_value_relevant, 'tag_table': tag_table, 'relative_table_elements': number_td_type_per_word, 'height_width_diff': diff_height_width}
    df = DataFrame(data)
    writer = ExcelWriter('First Iteration Data\data_gathered_part_second_segmentation_3.xlsx', engine = 'openpyxl')
    df.to_excel(writer, sheet_name = 'Sheet1', header = True)
    writer.save()

def extractFrom(content, URI):
    soup_object = BeautifulSoup(content, 'lxml')
    driver = webdriver.Firefox(executable_path=r'D:\Softwares\Anaconda\Anaconda\geckodriver-v0.24.0-win64\geckodriver.exe')
    driver.get(URI)
    # time.sleep(5)
    root_x_path = xpath_soup(soup_object.body)
    root_element = driver.find_element_by_xpath(root_x_path)
    root_width = root_element.size.get('width')
    root_height = root_element.size.get('height')
    featureExtraction(soup_object.body.findAll('div', {'class' : 'mw-body'}), driver, root_width, root_height)
    formCSVData()
    driver.quit()
    clearAll()

f = open('List Of Sites\Wikipedia\site_3.html', 'r', encoding = 'utf8', errors = 'ignore')
URI = 'file:///D:/Passion/Machine%20Learning/Projects/Semantic_Web_Parser_Model_Builder/Second%20Model%20Preparation/List%20of%20Sites/Wikipedia/site_3.html'
content = f.read()
f.close()
extractFrom(content, URI)