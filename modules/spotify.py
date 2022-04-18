import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Scopes to allow
SCOPES = "user-read-private,user-read-currently-playing,user-read-playback-state"

client = None

#
# Authorize and create client
#
def authorize():
  global client
  client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPES))

#
# Get now playing data
#
def get_now_playing():
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
