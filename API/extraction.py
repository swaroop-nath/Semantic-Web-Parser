from bs4 import BeautifulSoup as BS
from bs4 import NavigableString
from urllib import request as request
import pandas as pd
import numpy as np
import re
import pickle
from errors import NotExtractableError
from second_phase_model import SecondPhaseModel

regexp = '; |, | |\n|-\*'

def first_phase_filtration(soup):
    total_words = len(re.split(regexp, soup.body.text))
    total_p_tags = []
    for found in soup.body.findAll('p'):
        total_p_tags.append(found)
    total_p_tags = len(total_p_tags)

    queue = list(soup.children)

    model = None
    with open('first_model.mdl', 'rb') as file:
        model = pickle.load(file)

    while len(queue) > 0:
        features = {'Num Words': None, 'Fraction p Children': None}
        element = queue.pop(0)
        if isinstance(element, NavigableString): continue

        for child in element.children: queue.append(child)

        num_words = len(re.split(regexp, element.text))
        num_p_children = 0
        for tag in element.children:
            if tag.name == 'p': num_p_children += 1
        features['Num Words'] = num_words/total_words

        features['Fraction p Children'] = num_p_children/total_p_tags
        features['Interaction'] = features['Fraction p Children'] + features['Num Words']

        feature_vector = np.array([features['Fraction p Children'], features['Interaction']], dtype = float)
        label = model.predict(feature_vector.reshape(1, -1))
        if label == 1: return element

    return None

def second_phase_filtration(relevant_content):
    model = SecondPhaseModel()
    final_doc = model.transform(relevant_content)
    return final_doc

def extract_relevant_content(url):
    content = request.urlopen(url)
    soup = BS(content, 'lxml')

    relevant_content = first_phase_filtration(soup)
    if relevant_content is None: raise NotExtractableError('Internal error.\nCould not extract from the web-page')

    final_doc = second_phase_filtration(relevant_content)

    return final_doc