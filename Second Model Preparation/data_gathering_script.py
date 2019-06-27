import urllib.request as request
from bs4 import BeautifulSoup, NavigableString
import re
from pandas import DataFrame, ExcelWriter
from selenium import webdriver
import itertools
import time
from selenium.common.exceptions import NoSuchElementException as NSEE

header_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header']
paragraph_tags = ['p', 'i', 'b', 'u', 'em', 'small', 'strike', 'strong']
listing_tags = ['ul', 'li', 'ol', 'table']
image_classes = ['img', 'image']
regexp = '; |, | |\n|-\*'

tag_header = []
tag_para = []
tag_img = []
attr_src = []
class_image = []
element_area_ratio = []
word_count = []
coord_x = []
coord_y = []
width = []
height = []
has_listing_related = []
tag_aside = []
class_sidebar = []
child_img = []
child_text = []
name = []
attrs = []

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

def contains(string):
    if image_classes[0] in string or image_classes[1] in string: return True
    return False

def featureExtraction(soup, driver, root_area):
    tags = soup[0].find_all()
    for tag in tags:
        if not isinstance(tag, NavigableString):
            if tag.name in header_tags: tag_header.append('YES')
            else: tag_header.append('NO')
            
            if tag.name in paragraph_tags: tag_para.append('YES')
            else: tag_para.append('NO')
            
            if 'img' in tag.name: tag_img.append('YES')
            else: tag_img.append('NO')
            
            if 'src' in tag.attrs: attr_src.append('YES')
            else: attr_src.append('NO')
            
            if 'class' in tag.attrs and contains(tag.attrs.get('class')): class_image.append('YES')
            else: class_image.append('NO')
            
            if 'aside' in tag.name: tag_aside.append('YES')
            else: tag_aside.append('NO')
            
            if tag.name in listing_tags: has_listing_related.append('YES')
            else: has_listing_related.append('NO')
            
            if 'class' in tag.attrs and 'side' in tag.attrs.get('class'): class_sidebar.append('YES')
            else: class_sidebar.append('NO')

            text_content = tag.text.strip()
            word_list = re.split(regexp, text_content)
            word_count.append(len(word_list))

            x_path_tag = xpath_soup(tag)
            try:
                element = driver.find_element_by_xpath(x_path_tag)
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
            except NSEE:
                coord_x.append('nan')
                coord_y.append('nan')
                height.append('nan')
                width.append('nan')
                element_area_ratio.append('nan')
            
            children_tags = tag.children
            flag_text = False
            flag_img = False
            for child in children_tags:
                if child.name in paragraph_tags or child.name in header_tags: flag_text = True
                if 'img' == child.name: flag_img = True
            if flag_img: child_img.append('YES')
            else: child_img.append('NO')
            if flag_text: child_text.append('YES')
            else: child_text.append('NO')

            name.append(tag.name)
            attrs.append(list(tag.attrs.values()))


def clearAll():
    tag_header.clear()
    tag_para.clear()
    tag_img.clear()
    attr_src.clear()
    class_image.clear()
    element_area_ratio.clear()
    word_count.clear()
    coord_x.clear()
    coord_y.clear()
    width.clear()
    height.clear()
    has_listing_related.clear()
    tag_aside.clear()
    class_sidebar.clear()
    name.clear()
    attrs.clear()
        
def formCSVData():
    data = {'tag_header' : tag_header, 'tag_para' : tag_para, 'tag_img' : tag_img, 'attr_src' : attr_src, 'class_image' : class_image, 'element_area_ratio' : element_area_ratio, 'word_count' : word_count, 'x' : coord_x, 'y' : coord_y, 'width' : width, 'height' : height, 'has_listing_related' : has_listing_related, 'tag_aside' : tag_aside, 'class_sidebar' : class_sidebar, 'child_img' : child_img, 'child_text' : child_text,'name' : name, 'attrs' : attrs}
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
    root_area = root_element.size.get('width') * root_element.size.get('height')
    featureExtraction(soup_object.body.findAll('section', {'class' : 'blog-body'}), driver, root_area)
    formCSVData()
    driver.quit()
    clearAll()

f = open('List Of Sites\site_3.html', 'r', encoding = 'utf8', errors = 'ignore')
URI = 'file:///D:/Passion/Machine%20Learning/Projects/Semantic_Web_Parser_Model_Builder/Second%20Model%20Preparation/List%20of%20Sites/site_3.html'
content = f.read()
f.close()
extractFrom(content, URI)