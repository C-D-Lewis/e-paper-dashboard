import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
from modules import config

# Scopes to allow
SCOPES = "user-read-private,user-read-currently-playing,user-read-playback-state"

client = None
last_playing = {}

#
# Authorize and create client
#
def authorize():
  global client

  auth_manager = SpotifyOAuth(
    scope=SCOPES,
    client_id=config.get('SPOTIFY_CLIENT_ID'),
    client_secret=config.get('SPOTIFY_CLIENT_SECRET'),
    redirect_uri=config.get('SPOTIFY_REDIRECT_URI'),
    open_browser=False
  )
  client = spotipy.Spotify(auth_manager=auth_manager)

#
# Cache last data to disk
#
def cache_last():
  with open('last_playing.json', 'w') as outfile:
    json.dump(last_playing, outfile)

#
# Load cached data
#
def load_last():
  global last_playing

  with open('last_playing.json') as json_file:
    last_playing = json.load(json_file)

#
# Get now playing data
#
def get_now_playing():
  global last_playing

  try:
    data = client.current_playback()
    track = data['item']
    album = track['album']

    last_playing = {
      'track_name': track['name'],
      'album_name': album['name'],
      'artist_name': album['artists'][0]['name'],
      'album_image': album['images'][0]['url']
    }

    cache_last()
    print("spotify: cached")
    return last_playing
  except Exception as err:
    # Try the local cache
    try:
      load_last()
      print("spotify: loaded cache")
      return last_playing
    except Exception as err2:
      print(err2)
      return None
