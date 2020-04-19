from nltk import sent_tokenize
from urllib import request as request
from bs4 import BeautifulSoup

class SecondPhaseModel:
    def __init__(self, threshold = 1):
        self.threshold = threshold

    def transform(self, soup):
        main_content = soup.text

        paragraphs = main_content.split('\n')
        final_doc = ''
        for paragraph in paragraphs:
            sentences = sent_tokenize(paragraph)
            if len(sentences) > self.threshold: final_doc += paragraph + '\n\n'

        return final_doc