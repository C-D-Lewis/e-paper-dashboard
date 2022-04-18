import spotipy
from spotipy.oauth2 import SpotifyOAuth
from modules import config

# Scopes to allow
SCOPES = "user-read-private,user-read-currently-playing,user-read-playback-state"

client = None

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
# Get now playing data
#
def get_now_playing():
  try:
    data = client.current_playback()
    track = data['item']
    album = track['album']

    results = {
      'track_name': track['name'],
      'album_name': album['name'],
      'artist_name': album['artists'][0]['name'],
      'album_image': album['images'][0]['url']
    }

    return results
  except Exception as err:
    print(err)
    return None
