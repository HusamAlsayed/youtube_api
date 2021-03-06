import requests
import json
from youtube_transcript_api import YouTubeTranscriptApi

class Youtube:
  """
    an implementation to the youtube api so that you can use channel and videos .. 
  """
  def __init__(self,youtube_key,endpoint):
    """
      you have to specify the api token 
    """
    self.youtube_key = youtube_key
    self.endpoint = endpoint

  def get_channel_playlists(self,part,channel_id,page_token):

    """
      get a channel playlist here you take only one part if the number of channels bigger than the whole number of channel allowed .
    """
    url = self.endpoint + 'playlists?part={}&channelId={}&key={}&pageToken={}'
    url = url.format(part,channel_id,self.youtube_key,page_token)
    data = requests.get(url)
    return data.json()
  

  def get_all_playlists(self,part,channel_id):

    """
      get all the playlists .. 
    """
    play_lists = []
    page_token = ''
    while True:
      ok = False
      d = self.get_channel_playlists('snippet',channel_id,page_token)
      if 'nextPageToken' in  d:
        ok = True
        page_token = d['nextPageToken']
      for l in d['items']:
        play_lists.append(l)

      if ok == False:
        break

    return play_lists


  def get_playlist_videos(self,part,playlist,page_token):
    """
      get part of the videos in the database .. 
    """
    url = self.endpoint + 'playlistItems?part={}&playlistId={}&key={}&pageToken={}'
    url = url.format(part,playlist,self.youtube_key,page_token)
    data = requests.get(url)
    return data.json()

  def get_all_playlist_videos(self,part,playlists):
    """
      get the whole videos of a certain playlist .. 
    """
    playlists_videos = []
    for playlist in playlists:
      page_token = ''
      small_data = {}
      small_data['playlist_id'] = playlist['id']
      small_data['videos'] = []
      while True:
        ok = False
        d = self.get_playlist_videos('snippet',playlist['id'],page_token)
        if 'nextPageToken' in d:
          ok = True
          page_token = d['nextPageToken']
        
        for l in d['items']:
          small_data['videos'].append(l)
        
        
        if ok == False:
          break
      playlists_videos.append(small_data)
    
    return playlists_videos

  @staticmethod
  def get_video_transcript(video_url):
    begin = 'https://www.youtube.com/watch?v='
    l = len(begin)
    if video_url.startswith(begin):
       video_url = video_url[l:]
    trans = YouTubeTranscriptApi.get_transcript(video_url, languages=['en'])
    data = []
    for item in trans:
        x = json.dumps(item)
        y = json.loads(x)
        data.append(y)
    return data



  @staticmethod
  def get_word_time_transcript(video_url):
    data = Youtube.get_video_transcript(video_url)
    newjson = {}
    newjson['transcripts'] = []
    for i in data:
        text = i['text']
        duration = i['duration']
        words = text.split()
        l = len(words)
        for w in range(len(words)):
            newtime = i['start'] + w * (duration / l)
            newjson['transcripts'].append({'word': words[w], 'start_time ': newtime})
    return newjson


  
