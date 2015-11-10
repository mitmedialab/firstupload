# -*- coding: utf-8 -*-
from __future__ import print_function
import pafy
import tweepy
import re
import requests
import pprint
import codecs
import json
import os

import requests


#!/usr/bin/env python

#	Copyright 2013 AlchemyAPI
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.



try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
    from urllib.parse import urlencode
except ImportError:
    from urlparse import urlparse
    from urllib2 import urlopen
    from urllib import urlencode

try:
    import json
except ImportError:
    # Older versions of Python (i.e. 2.4) require simplejson instead of json
    import simplejson as json



if __name__ == '__main__':
    """
    Writes the API key to api_key.txt file. It will create the file if it doesn't exist.
    This function is intended to be called from the Python command line using: python alchemyapi YOUR_API_KEY
    If you don't have an API key yet, register for one at: http://www.alchemyapi.com/api/register.html

    INPUT:
    argv[1] -> Your API key from AlchemyAPI. Should be 40 hex characters

    OUTPUT:
    none
    """

    import sys
    if len(sys.argv) == 2 and sys.argv[1]:
        if len(sys.argv[1]) == 40:
            # write the key to the file
            f = open('api_key.txt', 'w')
            f.write(sys.argv[1])
            f.close()
            print('Key: ' + sys.argv[1] + ' was written to api_key.txt')
            print(
                'You are now ready to start using AlchemyAPI. For an example, run: python example.py')
        else:
            print('The key appears to invalid. Please make sure to use the 40 character key assigned by AlchemyAPI')


class AlchemyAPI:
    # Setup the endpoints
    ENDPOINTS = {}
    ENDPOINTS['keywords'] = {}
    ENDPOINTS['keywords']['url'] = '/url/URLGetRankedKeywords'
    ENDPOINTS['keywords']['text'] = '/text/TextGetRankedKeywords'
    ENDPOINTS['keywords']['html'] = '/html/HTMLGetRankedKeywords'
    ENDPOINTS['concepts'] = {}
    ENDPOINTS['concepts']['url'] = '/url/URLGetRankedConcepts'
    ENDPOINTS['concepts']['text'] = '/text/TextGetRankedConcepts'
    ENDPOINTS['concepts']['html'] = '/html/HTMLGetRankedConcepts'
    ENDPOINTS['entities'] = {}
    ENDPOINTS['entities']['url'] = '/url/URLGetRankedNamedEntities'
    ENDPOINTS['entities']['text'] = '/text/TextGetRankedNamedEntities'
    ENDPOINTS['entities']['html'] = '/html/HTMLGetRankedNamedEntities'
    ENDPOINTS['language'] = {}
    ENDPOINTS['language']['url'] = '/url/URLGetLanguage'
    ENDPOINTS['language']['text'] = '/text/TextGetLanguage'
    ENDPOINTS['language']['html'] = '/html/HTMLGetLanguage'

    # The base URL for all endpoints
    BASE_URL = 'http://access.alchemyapi.com/calls'

    s = requests.Session()

    def __init__(self):
        """	
        Initializes the SDK so it can send requests to AlchemyAPI for analysis.
        It loads the API key from api_key.txt and configures the endpoints.
        """

        import sys
        key = os.environ.get("ALCHEMY_KEY")
        if key == '':
            # The key file should't be blank
            print(
                'The API key variable (os.ALCHEMY_KEY) seems to be blank. Please add environment variable for the API key.')
            print(
                'If you do not have an API Key from AlchemyAPI, please register for one at: http://www.alchemyapi.com/api/register.html')
            sys.exit(0)
        elif len(key) != 40:
            # Keys should be exactly 40 characters long
            print(
                'It appears that the api key variable (os.ALCHEMY_KEY) is invalid. Please make sure the key is the correct one.')
            sys.exit(0)
        else:
            # setup the key
            self.apikey = key

    def entities(self, flavor, data, options={}):
        """
        Extracts the entities for text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/entity-extraction/ 
        For the docs, please refer to: http://www.alchemyapi.com/api/entity-extraction/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        disambiguate -> disambiguate entities (i.e. Apple the company vs. apple the fruit). 0: disabled, 1: enabled (default)
        linkedData -> include linked data on disambiguated entities. 0: disabled, 1: enabled (default) 
        coreference -> resolve coreferences (i.e. the pronouns that correspond to named entities). 0: disabled, 1: enabled (default)
        quotations -> extract quotations by entities. 0: disabled (default), 1: enabled.
        sentiment -> analyze sentiment for each entity. 0: disabled (default), 1: enabled. Requires 1 additional API transction if enabled.
        showSourceText -> 0: disabled (default), 1: enabled 
        maxRetrieve -> the maximum number of entities to retrieve (default: 50)

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['entities']:
            return {'status': 'ERROR', 'statusInfo': 'entity extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['entities'][flavor], {}, options)

    def keywords(self, flavor, data, options={}):
        """
        Extracts the keywords from text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/products/features/keyword-extraction/
        For the docs, please refer to: http://www.alchemyapi.com/api/keyword-extraction/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        keywordExtractMode -> normal (default), strict
        sentiment -> analyze sentiment for each keyword. 0: disabled (default), 1: enabled. Requires 1 additional API transaction if enabled.
        showSourceText -> 0: disabled (default), 1: enabled.
        maxRetrieve -> the max number of keywords returned (default: 50)

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['keywords']:
            return {'status': 'ERROR', 'statusInfo': 'keyword extraction for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['keywords'][flavor], {}, options)

    def language(self, flavor, data, options={}):
        """
        Detects the language for text, a URL or HTML.
        For an overview, please refer to: http://www.alchemyapi.com/api/language-detection/ 
        For the docs, please refer to: http://www.alchemyapi.com/products/features/language-detection/

        INPUT:
        flavor -> which version of the call, i.e. text, url or html.
        data -> the data to analyze, either the text, the url or html code.
        options -> various parameters that can be used to adjust how the API works, see below for more info on the available options.

        Available Options:
        none

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Make sure this request supports this flavor
        if flavor not in AlchemyAPI.ENDPOINTS['language']:
            return {'status': 'ERROR', 'statusInfo': 'language detection for ' + flavor + ' not available'}

        # add the data to the options and analyze
        options[flavor] = data
        return self.__analyze(AlchemyAPI.ENDPOINTS['language'][flavor], {}, options)

    def __analyze(self, endpoint, params, post_data=bytearray()):
        """
        HTTP Request wrapper that is called by the endpoint functions. This function is not intended to be called through an external interface. 
        It makes the call, then converts the returned JSON string into a Python object. 

        INPUT:
        url -> the full URI encoded url

        OUTPUT:
        The response, already converted from JSON to a Python object. 
        """

        # Add the API Key and set the output mode to JSON
        params['apikey'] = self.apikey
        params['outputMode'] = 'json'
        # Insert the base url

        post_url = ""
        try:
            post_url = AlchemyAPI.BASE_URL + endpoint + \
                '?' + urlencode(params).encode('utf-8')
        except TypeError:
            post_url = AlchemyAPI.BASE_URL + endpoint + '?' + urlencode(params)

        results = ""
        try:
            results = self.s.post(url=post_url, data=post_data)
        except Exception as e:
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'network-error'}
        try:
            return results.json()
        except Exception as e:
            if results != "":
                print(results)
            print(e)
            return {'status': 'ERROR', 'statusInfo': 'parse-error'}

def removeURLs(description):
    description_noURL = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}     /)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', description)
    return description_noURL

access_token = os.environ.get("TWEEPY_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWEEPY_ACCESS_TOKEN_SECRET")
consumer_key = os.environ.get("TWEEPY_CONSUMER_KEY")
consumer_secret = os.environ.get("TWEEPY_CONSUMER_SECRET")
alchemy_key = os.environ.get("ALCHEMY_KEY")

#Oauth stuff
tweepy_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
tweepy_auth.set_access_token(access_token, access_token_secret)

#initialize tweepy API object
tweepy_api = tweepy.API(tweepy_auth)

def twitterSearch(url):
    query = url
    tweets = ''
    for tweet in tweepy.Cursor(tweepy_api.search,q=query).items():
        #avoid UnicodeEncodeError:
        #status = tweet.text.encode('ascii','ignore')
        status_without_URLs = removeURLs(tweet.text)
        tweets += status_without_URLs + '\n'
    return tweets

newobject = AlchemyAPI()
    