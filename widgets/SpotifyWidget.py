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

  #
  # Update latest now playing information
  #
  def update_data(self):
    try:
      # Check auth
      authorize()

      # Fetch now playing data
      new_data = get_now_playing()
      if not new_data:
        print("[spotify] nothing is playing")
        raise Exception('Nothing is playing')
      self.track_data = new_data

      # Fetch image and convert
      img_data = urllib.request.urlopen(self.track_data['album_image']).read()
      self.album_image = Image.open(BytesIO(img_data)).resize((IMAGE_SIZE, IMAGE_SIZE)).convert('RGBA')

      print(f"[spotify] {self.track_data}")
      self.unset_error()
    except Exception as err:
      self.set_error(err)

  #
  # Draw the now playing information
  #
  def draw_data(self, image_draw, image):
    root_x = self.bounds[0]
    root_y = self.bounds[1] + 5
    text_x = root_x + IMAGE_SIZE + 6
    max_line_width = SPOTIFY_BOUNDS[2] - text_x
    text_gap = 25

    # Album image
    if self.album_image != None:
      image.paste(self.album_image, (root_x, root_y))

    # Artist name
    artist_name_str = self.track_data['artist_name']
    lines = helpers.get_wrapped_lines(artist_name_str, fonts.KEEP_CALM_20, max_line_width)[:2]
    if len(lines) > 1:
      for index, line in enumerate(lines):
        image_draw.text((text_x, root_y + 5 + (index * text_gap)), line, font = fonts.KEEP_CALM_20, fill = 0)
    else:
      image_draw.text((text_x, root_y + 5), artist_name_str, font = fonts.KEEP_CALM_20, fill = 0)

    # Track name
    track_name_str = self.track_data['track_name']
    lines = helpers.get_wrapped_lines(track_name_str, fonts.KEEP_CALM_24, max_line_width)[:2]
    if len(lines) > 1:
      for index, line in enumerate(lines):
        image_draw.text((text_x, root_y + 55 + (index * text_gap)), line, font = fonts.KEEP_CALM_24, fill = 0)
    else:
      image_draw.text((text_x, root_y + 55), track_name_str, font = fonts.KEEP_CALM_24, fill = 0)

    # Album name
    album_name_str = self.track_data['album_name']
    image_draw.text((text_x, root_y + 110), album_name_str, font = fonts.KEEP_CALM_20, fill = 0)
