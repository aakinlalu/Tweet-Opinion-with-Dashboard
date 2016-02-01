# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 13:50:15 2016

@author: Adebayo
"""

# coding: utf-8

# ## DEVELOP DATA VISUALIZATION ON EXTRACTED TWEETS  
# ### Required Tools
# 1. Python
# 2. Mongodb
# ### Processes
# 1. Extract tweets using Python library(tweepy)
# 2. Store the tweet in database(Mongodb)
# 3. Query the tweet with python
# 4. Develop Visualizations on the Query
# 6. Present the visualization dashboard through web framework
# ---
# 

from tweepy import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient
import json

#This is a listener that send recieved tweets to database
class sendListenerOut(StreamListener):
    """
    StreamListener is a class provided by library(tweepy) used to acesss
    the Twitter Streaming API. It provides real-time tweets retrieval.
    """
    def on_connect(self):
        """When the connection is made"""
        print "It is connected to the streaming server"
    
    def on_error(self, status):
        """When error occurs"""
        print "Error:" + repr(status)
        return False
    
    def on_data(self, data):
        """It is called each time stream data is recieved"""
        client = MongoClient('localhost', 27017)
        
        #Use tweetdb database
        db = client
        
        #Decode JSOn
        tweetJson = json.loads(data)
        
        #Store tweet into the tweetcollect collection
        db.tweetcollect.insert(tweetJson)

#Create function to authenticated access to twitter
def accessAuth(credentialPath):
    '''
    AccessAuth function will provide authenticated access to twitter
    using stored credential
    '''
    with open(credentialPath, 'r') as conn:
        line = conn.read().split(',')
    consumer_key = line[0]
    consumer_secret = line[1]
    access_token = line[2]
    access_token_secret = line[3]
    
    authentication = OAuthHandler(consumer_key, consumer_secret)
    authentication.set_access_token(access_token, access_token_secret)
    return authentication
    
    #load credential 
def streaming(keywords, credentialPath):
    """
    It handles Twitter authetification and the connection to Twitter Streaming API.
    And to filter Twitter Streams to capture data by the keywords.
    keywords is a list
    """
    l = sendListenerOut()
    auth = accessAuth(credentialPath)
    stream = Stream(auth, l)
    stream.filter(track=keywords)

if __name__ == '__main__':
    credentialPath = 'credential.txt'
    keywords = ["war", "middle east", "asylum seeker"]
    stream = streaming(keywords,credentialPath)