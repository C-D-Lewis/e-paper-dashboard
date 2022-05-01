import urllib
from PIL import Image
from io import BytesIO
from modules import fonts, helpers
from widgets.Widget import Widget
from modules.constants import WIDGET_BOUNDS
from modules.spotify import authorize, get_now_playing

WIDGET_BOUNDS_LEFT_TOP = WIDGET_BOUNDS[0]
WIDGET_BOUNDS_LEFT_HALF = WIDGET_BOUNDS[3]
SPOTIFY_BOUNDS = WIDGET_BOUNDS_LEFT_HALF

# Image icon size
IMAGE_SIZE_LEFT_TOP = 128
IMAGE_SIZE_LEFT_HALF = 200
IMAGE_SIZE = IMAGE_SIZE_LEFT_HALF

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
  # Draw the now playing information in the left top slot
  #
  def draw_data_left_top(self, image_draw, image):
    root_x = self.bounds[0]
    root_y = self.bounds[1] + 5
    text_x = root_x + IMAGE_SIZE + 6
    max_line_width = SPOTIFY_BOUNDS[2] - text_x
    text_gap = 25

    # Album image
    if self.album_image != None:
      image.paste(self.album_image, (root_x, root_y))

    # Artist name
    helpers.draw_wrapped_text_lines(
      image_draw,
      self.track_data['artist_name'],
      fonts.KEEP_CALM_20,
      (text_x, root_y + 5),
      gap=text_gap,
      max_width=max_line_width,
      max_lines=2
    )

    # Track name
    helpers.draw_wrapped_text_lines(
      image_draw,
      self.track_data['track_name'],
      fonts.KEEP_CALM_24,
      (text_x, root_y + 55),
      gap=text_gap,
      max_width=max_line_width,
      max_lines=2
    )

    # Album name
    helpers.draw_wrapped_text_lines(
      image_draw,
      self.track_data['album_name'],
      fonts.KEEP_CALM_20,
      (text_x, root_y + 110),
      gap=text_gap,
      max_width=max_line_width,
      max_lines=1
    )

  #
  # Draw the now playing information in the left half
  #
  def draw_data_left_half(self, image_draw, image):
    root_x = self.bounds[0]
    root_y = self.bounds[1] + 5
    image_x = round((self.bounds[2] - IMAGE_SIZE) / 2)
    text_x = root_x + IMAGE_SIZE + 6
    max_line_width = SPOTIFY_BOUNDS[2] - text_x
    text_gap = 25

    # Album image
    if self.album_image != None:
      image.paste(self.album_image, (image_x, root_y))

    # Artist name

    # Track name

    # Album name

  #
  # Draw spotify now-playing data
  #
  def draw_data(self, image_draw, image):
    # One of (TODO: Add to config)
    # self.draw_data_left_top(image_draw, image)
    self.draw_data_left_half(image_draw, image)
