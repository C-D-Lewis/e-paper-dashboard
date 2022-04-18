import urllib
from PIL import Image, ImageDraw, ImageOps
from io import BytesIO
from modules import fetch, fonts, config, helpers, images
from widgets.Widget import Widget
from modules.constants import WIDGET_BOUNDS
from modules.spotify import authorize, get_now_playing

SPOTIFY_BOUNDS = WIDGET_BOUNDS[0]

# Image icon size
IMAGE_SIZE = 128

#
# SpotifyWidget class
#
class SpotifyWidget(Widget):
  #
  # Constructor
  #
  def __init__(self):
    super().__init__(SPOTIFY_BOUNDS)

    self.track_data = {
      'track_name': '',
      'album_name': '',
      'artist_name': '',
      'album_image': '',
    }
    self.album_image = None

  # Update latest now playing information
  def update_data(self):
    try:
      # Check auth
      authorize()

      # Fetch now playing data
      self.track_data = get_now_playing()

      # Fetch image and convert
      img_data = urllib.request.urlopen(self.track_data['album_image']).read()
      self.album_image = Image.open(BytesIO(img_data)).resize((IMAGE_SIZE, IMAGE_SIZE)).convert('RGBA')

      print(f"spotify: {self.track_data}")
      self.unset_error()
    except Exception as err:
      self.set_error(err)

  # Draw the news stories
  def draw(self, image_draw, image):
    if self.error:
      self.draw_error(image_draw)
      return

    try:
      root_y = self.bounds[1] + 5
      line_gap_y = 25

      # Album image
      if self.album_image != None:
        image.paste(self.album_image, (self.bounds[0], root_y))

      # Album name

      # Track name

      # Artist name

    except Exception as err:
      self.set_error(err)
      self.draw_error(image_draw)
