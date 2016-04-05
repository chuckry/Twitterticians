#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import json
import time
import re
import nltk
import pandas as pd
import vincent as v
import csv
import numpy as np
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf8')
stemmer = nltk.stem.PorterStemmer()

consumer_key = 'V0W3LRpP3JNun2ABqneoj6mUH'
consumer_secret = 'L9qypAfcoBe0bPsIm3LwkQG7ONhYAFOUzS8GX4RpNx6xLazudN'
access_token = '142690005-ocZzF6Fh8IqLLQQW2vBBjQKz0DtQDFkIX46xjUaX'
access_token_secret = 'aF1t4VjdP7CCMLboe7s7latKqimGDirmPus3UWJTXpzQB'

keyword_list = ['#BernieSanders']

start_time = time.time()

class listener(tweepy.StreamListener):
    def __init__(self, start_time, time_limit):
        self.time = start_time
        self.limit = time_limit
        self.tweet_data = []

    def on_data(self, data):
        while (time.time() - self.time) < self.limit:
            try:
                decoded = json.loads(data)
                data_write = json.dumps({'user': decoded['user']['screen_name'], 'time': decoded['created_at'], 'tweet': decoded['text']}).encode('utf-8')
                self.tweet_data.append(data_write)
                self.tweet_data.append('\n')
                print data_write
                return True
            except BaseException, e:
                print "failed on_data," , str(e)
                print data
            return True

        with open('Bernie_amilly_rawtweets.json', 'w') as rawt:
            for line in self.tweet_data:
                rawt.write(line)
        return False

    def on_error(self, status):
            print status
            return True

#Specify time-limits to Twitter streaming listener
if __name__ == '__main__':
    #Will listen Twitter stream for 1200 seconds
    l = listener(start_time, time_limit=60)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)



# print "Showing all new tweets:"
# stream = tweepy.Stream(auth, l)
# # Listen to Twitter streaming data for the given keyword. Narrow it down to English.
# stream.filter(track=keyword_list, languages=['en'])

with open("Bernie_amilly_rawtweets.json", 'rU') as json_file:
    twitter_data = []
    for line in json_file:
        twitter_data.append(json.loads(line))

def tweet_filter(tweet, stemmer):
    tweet = tweet.decode('utf-8').strip()
    tweet = tweet.lower()
    #i['tweet'] = re.sub(r'https?://\w+\W\w+/\w+.[a-zA-Z0-9]/?[a-zA-Z0-9]\b', 'URL ', i['tweet'])
    tweet = re.sub(r'(https?:\\|https?://|https?:|http:?)[^\s]+', 'URL ', tweet)
    tweet = re.sub(r'@([A-Za-z0-9_]+)', 'AT_USER', tweet)
    tweet = re.sub(r'#','', tweet)
    tweet = re.sub(r'\.{2,}','.', tweet)
    tweet = re.sub(r'\!{2,}','!', tweet)
    tweet = re.sub(r'\,{2,}',',', tweet)
    tweet = re.sub(r'\'{2,}',"'", tweet)
    tweet = re.sub(r'\:{2,}',':', tweet)
    tweet = re.sub(r'\"{2,}','"', tweet)
    otweet = stemmer.stem(tweet)
    return otweet

def extract_feature(text, size = 1, size2 = 2):
    tokens = text.split()
    features = {}
    for i in range(0, tokens.__len__()-size+1):
        feature = '+' .join(tokens[i:i+size])
        if features.has_key(feature):
            features[feature] += 1
        else:
            features[feature] = 1
    for i in range(0, tokens.__len__()-size2+1):
        feature = '+' . join(tokens[i:i+size2])
        if features.has_key(feature):
            features[feature] += 1
        else:
            features[feature] = 1
    return features

def load_training_data():
    csv_read = csv.reader(codecs.open('Sentiment_Analysis_Dataset.csv', 'rb'), delimiter =',')
    csv_read.next()
    label = []
    for tweet in csv_read:
        if tweet[1] == 1:
            tweet[1] = 'positive'
        else:
            tweet[1] = 'negative'
        feature = extract_feature(tweet_filter(tweet[3], stemmer))
        #print feature
        if feature != None:
            label.append((feature,tweet[1]))



    train, test = label[:int(len(label)*0.9)], label[int(len(label)*0.1):]
    print nltk.classify.accuracy(nltk.NaiveBayesClassifier.train(label), test)
    classifier = nltk.NaiveBayesClassifier.train(label)
    return classifier

def sentiment_analysis(classifier):
    sfp = codecs.open('Bernie_amilly_labelledtweets.json', 'w')
    tweets = codecs.open('Bernie_amilly_cleanedtweets.json')
    for tweet in tweets:
        tweet = json.loads(tweet)
        label = extract_feature(tweet['tweet'])
        classed = classifier.classify(label)
        tweet['sentiment'] = classed
        sfp.write(json.dumps(tweet) + '\n')

clean = codecs.open('Bernie_amilly_cleanedtweets.json', 'w')
for line in twitter_data:
    line['tweet'] = tweet_filter(line['tweet'], stemmer)
    clean.write(json.dumps(line) + '\n')
clean.close()

# def custom_ressampler(arr, size):
#     return np.sum(arr)/size

# def time_series_tweets():
#     with open('Bernie_amilly_labelledtweets.json') as graph_file:
#         data = dict()
#         time_array = []
#         pta = []
#         for line in graph_file:
#             data = json.loads(line)
#             time_array.append(data['time'])
#             if data['sentiment'] == 'positive':
#                 pta.append(data['time'])
#     ones = [1]*len(time_array)
#     idx = pd.DatetimeIndex(time_array)
#     time_array = pd.Series(ones, index=idx)

#     time_array = time_array.resample('5s', how='sum').fillna(0)
#     time_chart = v.Line(time_array)
#     time_chart.axis_titles(x='Time', y="Freq")
#     time_chart.to_json('term_freq.json')


    # ones = [1]*len(pta)
    # idx = pd.DatetimeIndex(pta)
    # pta = pd.Series(ones, index=idx)
    # #pta = pta.resample('5s', how=custom_ressampler(pta, len(time_array)).fillna(0)
    # pta = pta.resample('5s', how='sum').fillna(0)
    # pta_chart = v.Line(pta)
    # pta_chart.axis_titles(x='Time', y='Freq of pos')
    # pta_chart.to_json('term_freq.json')



sentiment_analysis(load_training_data())

# time_series_tweets()