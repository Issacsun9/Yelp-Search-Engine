# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 14:06:43 2022

@author: Mingshu Li
"""
import string, json, csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
import re
#%% For text pre-processing
class TextPro:
    def __init__(self,review):
        self.rev = review
    def lowercase(self):
        self.rev = self.rev.lower()    
    def clean_url(self):
        self.rev = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', self.rev)
        self.rev = re.sub('www.[^s]+','', self.rev)    
    def cleaning_punctuations(self):
        punctuation_dict = {punc: ' ' for punc in string.punctuation}
        translator = str.maketrans(punctuation_dict)
        self.rev = self.rev.translate(translator)
    def clean_stopword(self):
        stop_word_part1 = nltk.corpus.stopwords.words('english')
        stop_word_part2 = ['a', 'about', 'above', 'after', 'again', 'ain', 'all', 'am', 'an','and','any','are', 'as', 'at', 'be', 
                   'because', 'been', 'before', 'being', 'below', 'between','both', 'by', 'can', 'd', 'did', 'do', 'does', 
                   'doing', 'down', 'during', 'each','few', 'for', 'from', 'further', 'had', 'has', 'have', 'having', 'he',
                   'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'im', 'if', 'in', 'into','is', 'it', 
                   'its', 'itself', 'just', 'll', 'm', 'ma', 'may', 'me', 'more', 'most', 'might', 'my', 'myself', 'now', 'o', 
                   'of', 'on','once','only', 'or', 'other', 'our', 'ours','ourselves', 'out', 'own', 'r', 're','s', 'same', 'she', "shes",
                   'should', "shouldve",'so', 'some', 'such', 't', 'than', 'that', "thatll", 'the', 'their', 'theirs', 'them', 
                   'themselves', 'then', 'there', 'these', 'they', 'this', 'those','through', 'to', 'too', 'u', 'under', 'until', 
                   'up', 've', 'very', 'was', 'we', 'were', 'what', 'when', 'where','which','while', 'who', 'whom','why',
                   'will', 'with', 'won', 'would', 'y', 'yall', 'you', "youd", "youll", "youre", "youve", 'your', 'yours', 
                   'yourself', 'yourselves']
        stop_word = stop_word_part1 + list(set(stop_word_part2) - set(stop_word_part1))
        self.rev = " ".join([word for word in str(self.rev).split() if word not in stop_word])
    def clean_numbers(self):
        self.rev = re.sub('[0-9]+', '', self.rev)
    def tokenize(self):
        tokenizer = nltk.tokenize.RegexpTokenizer('\s+', gaps = True)
        self.rev = tokenizer.tokenize(self.rev)
    def stem(self):#choose between stem, lemmatize, or both of them
        stemer = nltk.PorterStemmer()
        self.rev = [stemer.stem(wd) for wd in self.rev]        
    def lemmatize(self):
        lemmatizer = nltk.stem.WordNetLemmatizer()
        self.rev = [lemmatizer.lemmatize(wd) for wd in self.rev]  
    def output_list(self):#output list
        return self.rev
    def output_str(self):#output str
        return ' '.join(map(str, self.rev)).replace('[',"").replace(']',"").replace("'","").replace(",","")
#%%
if __name__ == '__main__':
    review = 'The food is not too bad. And the restaurant itself feels like an old chinese restaurant. I got confused when I saw spaghetti meatballs in the menu since its a chinese restaurant and decided to try. Well it 9 nine http://www.123.com.'   
    model_instance = TextPro(review)
    model_instance.lowercase()
    model_instance.clean_url()
    model_instance.cleaning_punctuations()
    model_instance.clean_stopword()
    model_instance.clean_numbers()
    model_instance.tokenize()
    #model_instance.stem()
    model_instance.lemmatize()
    new_list = model_instance.output_list()#call output_list() to output a list of words
    new_str = model_instance.output_str()#call outpu_str() to output string
