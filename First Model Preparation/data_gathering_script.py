from bs4 import BeautifulSoup as BS
from bs4 import NavigableString
from urllib import request as request
import pandas as pd
import numpy as np
import re
import os
from pathlib import Path
import itertools
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException as NSEE

tags = ['p', 'b', 'i', 'em', 'strong', 'sup', 'sub', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
regexp = '; |, | |\n|-\*'

def extract_features(soup, total_formatting_tags, total_tags_in_dom, total_words, total_p_tags, index):
    data_frame = pd.DataFrame(columns = ['Fraction Formatting Tags', 'Num Formatting Tags', 'Fraction Words', 'Num Words', 'name', 'attrs'])
    queue = list(soup.children)

    while len(queue) > 0:
        features = {'Fraction Formatting Tags': None, 'Fraction Words': None, 'Num Formatting Tags': None, 'Num Words': None, 'Fraction p Children': None, 'name': None, 'attrs': None}
        element = queue.pop(0)
        if isinstance(element, NavigableString): continue

        for child in element.children: queue.append(child)
        
        formatting_tags = []
        for tag in tags:
            for found in element.findAll(tag): formatting_tags.append(found)
        total_tags = len(element.findAll())
        formatting_tags = len(formatting_tags)

        num_words = len(re.split(regexp, element.text))

        num_p_children = 0
        for tag in element.children:
            if tag.name == 'p': num_p_children += 1

        features['Num Formatting Tags'] = (formatting_tags/total_formatting_tags)
        features['Num Words'] = num_words/total_words

        if total_tags > 0: 
            features['Fraction Formatting Tags'] = (formatting_tags/total_formatting_tags)/(total_tags/total_tags_in_dom)
            features['Fraction Words'] = (num_words/total_words)/(total_tags/total_tags_in_dom)
        else: 
            features['Fraction Formatting Tags'] = 'nan'
            features['Fraction Words'] = 'nan'

        features['Fraction p Children'] = num_p_children/total_p_tags

        features['name'] = element.name
        features['attrs'] = element.attrs

        data_frame = data_frame.append(features, ignore_index=True)
            

    # data_dir = Path('/Data/')
    # with open(r'/Data/dataset_' + str(index) + '.csv', 'w+') as file:
    data_frame.to_csv(r'Data/dataset_' + str(index) + '.csv', index=False)


urls = ['https://en.wikipedia.org/wiki/Data_science', 'https://www.britannica.com/science/Newtons-laws-of-motion', 
'https://www.livescience.com/37115-what-is-gravity.html', 'https://www.kdnuggets.com/2020/02/deep-neural-networks.html',
'https://www.geeksforgeeks.org/how-to-get-started-with-game-development/', 'https://www.javatpoint.com/spring-tutorial',
'https://www.tutorialspoint.com/spring/index.htm', 'https://www.linkengineering.org/EngineeringDesign.aspx', 
'https://byjus.com/maths/statistics/', 'https://www.britannica.com/science/statistics',
'https://en.wikipedia.org/wiki/Supervised_learning', 'https://www.livescience.com/chinese-rocket-sold-for-millions-auction.html',
'https://litslink.com/blog/an-introduction-to-machine-learning-algorithms', 'https://www.kdnuggets.com/2020/03/most-useful-machine-learning-tools-2020.html',
'https://www.javatpoint.com/hibernate-tutorial', 'https://www.javatpoint.com/mapping-list-in-collection-mapping',
'https://www.javatpoint.com/jsp-tutorial', 'https://www.tutorialspoint.com/caffe2/caffe2_image_classification_using_pre_trained_model.htm',
'https://www.linkengineering.org/Explore/EngineeringDesign/5824.aspx', 'https://www.fast.ai/2019/07/08/fastai-nlp/',
'https://www.geeksforgeeks.org/skip-list/', 'https://www.geeksforgeeks.org/shortest-path-faster-algorithm/?ref=leftbar-rightbar',
'https://byjus.com/maths/probability/', 'https://byjus.com/maths/differential-equation/']

for index in range(20, len(urls)):
    url = urls[index]
    with request.urlopen(url) as content:
        soup = BS(content, 'lxml')

        total_formatting_tags = []
        for tag in tags:
            for found in soup.body.findAll(tag):
                total_formatting_tags.append(found)

        total_p_tags = []
        for found in soup.body.findAll('p'):
            total_p_tags.append(found)

        total_tags = soup.body.findAll()
        total_words = len(re.split(regexp, soup.body.text))
        total_formatting_tags = len(total_formatting_tags)
        total_p_tags = len(total_p_tags)
        total_tags = len(total_tags)

        extract_features(soup.body, total_formatting_tags, total_tags, total_words, total_p_tags, index)
