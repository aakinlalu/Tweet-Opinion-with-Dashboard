# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 19:03:17 2016

@Created by Adebayo
"""
from pymongo import MongoClient
#import json
from pandas import DataFrame


def mongoConnection():
    """
    To connect to the mongodb through client
    """
    
    connection = MongoClient('localhost', 27017)
    client = connection['tweetdb']
    collection = client['tweetcollect']
    tweet = collection.find({}, {'text':1, 'source':1,'retweet_count':1,'user':1,'lang':1, 'created_at':1,'place':1, '_id':0})   
    return tweet
    
#we will structure the tweets data into a pandas DataFrame to simplify the data manipulation            
def createDataframe():
    tweet = DataFrame()
    tweetlist = [doc for doc in mongoConnection()]
    tweet['text'] = map(lambda x: x.get('text'), tweetlist)
    tweet['source'] = map(lambda x:x.get('source'), tweetlist)
    tweet['retweet_count'] = map(lambda x:x.get('retweet_count'), tweetlist)
    tweet['followers_count'] = map(lambda x:x.get('user')['followers_count'] if x.get('user') != None else 0, tweetlist)
    tweet['friends_count'] = map(lambda x:x.get('user')['friends_count'] if x.get('user') != None else 0, tweetlist)
    tweet['screen_name'] = map(lambda x:x.get('user')['screen_name'] if x.get('user') != None else 0, tweetlist)
    tweet['lang'] = map(lambda x:x.get('lang'), tweetlist)
    tweet['created_at'] = map(lambda x:x.get('created_at'), tweetlist)
    tweet['country'] = map(lambda x: x.get('place')['country'] if x.get('place') != None else None, tweetlist)
    return tweet
    


    
        