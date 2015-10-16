# -*- coding: utf-8 -*-
#!/flask/bin/python

import os
import sys

from apiclient.discovery import build, build_from_document
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import simplejson
import urllib
import datetime

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

DEVELOPER_KEY = os.environ.get("DEVELOPER_KEY")



def youtube_search(query):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=query,
    part="id,snippet",
    maxResults=20
  ).execute()

  videos = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      time = search_result["snippet"]["publishedAt"]
      time = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.000Z')
      data = {'title':search_result["snippet"]["title"], 'time':time, 'link':search_result["id"]["videoId"]}

      videos.append(data)

  orderedvideos = sorted(videos, key=lambda k: k['time']) 
  return orderedvideos



#youtube_search('meteorite crash Courtesy Urals region Russia Urals')

#title_from_id('IOHJBFiqchk')

