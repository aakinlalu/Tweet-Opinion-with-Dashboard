# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 11:31:52 2016

@author: adebayo
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns
import conn
from stop_words import get_stop_words
sns.set(color_codes=True)
reload(conn)

#Processing
def processing(tweet):
    '''
    Convert the tweets to the lowercase
    Convert any www.* or https?://* to url
    Convert @username to user
    Remove additional white spaces
    Replaces #word with word
    trim the tweet
    '''
    if tweet!= None:
        
        tweet = tweet.encode('utf8')
        tweet = tweet.lower()
        regex = '((www\.[^\s]+)|(https?://[^\s]+))'
        regex2 = '@[^\s]+'
        regex3 = '[\s]+'
        regex4 = r'#([^\s]+)'
        tweet = re.sub(regex, 'url', tweet)
        tweet = re.sub(regex2, 'at_user', tweet)
        tweet = re.sub(regex3, ' ', tweet)
        tweet = re.sub(regex4, r'\1', tweet)
        tweet = tweet.strip('\'"')
    return tweet

# load the tweet andprocesses


# - filtering tweets words for teature vector

stopWords = []

#Replace functions
def replacefn(char):
    '''
    replace the repetitive characters with itseft
    '''
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1",char)

def stopWord():
    '''These words don not indicate any sentiment and can be removed
    Repeating letter e.g hungrryyy for hungry
    Punctuation
    '''
    stopWords = get_stop_words('en')
    stopWords.append('at_user')
    stopWords.append('url') 
    return stopWords

def featureVector(tweet):
    featureVectorList = []
    regex = r'^[a-zA-Z][a-zA-Z0-9]*$'
    for char in tweet:
        if tweet is not None:
            char = tweet.split()
            char = replacefn(char).strip('\'"?,.')
            #chech if the word starts with an alphabet
            alphebet = re.search(regex, char)
            if char not in stopWord() or alphebet is not None:
                featureVectorList.append(char.lower())
            
    return featureVectorList

df = conn.createDataframe()
k = df['text'].map(lambda x:processing(x))
for num in np.arange(len(k)):
    x = k.iloc[num]
    print featureVector(x)

#print df['tweet'].map(lambda x: featureVector(x))
    
    