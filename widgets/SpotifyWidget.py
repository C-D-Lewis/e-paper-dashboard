import urllib
from PIL import Image
from io import BytesIO
from modules import fonts, helpers, log
from widgets.Widget import Widget
from modules.constants import WIDGET_BOUNDS_LEFT_TOP
from modules.spotify import authorize, get_now_playing

BOUNDS = WIDGET_BOUNDS_LEFT_TOP

# Image icon size
IMAGE_SIZE = 112

#
# SpotifyWidget class
#
class SpotifyWidget(Widget):
  #
  # Constructor
  #
  def __init__(self):
    super().__init__(BOUNDS)

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
        log.error('spotify', 'nothing is playing')
        raise Exception('Nothing is playing')
      self.track_data = new_data

      # Fetch image and convert
      img_data = urllib.request.urlopen(self.track_data['album_image']).read()
      self.album_image = Image.open(BytesIO(img_data)).resize((IMAGE_SIZE, IMAGE_SIZE)).convert('RGBA')

      log.info('spotify', self.track_data)
      self.unset_error()
    except Exception as err:
      self.set_error(err)

  #
  # Draw spotify now-playing data
  #
  def draw_data(self, image_draw, image):
    root_x = self.bounds[0] + 10
    root_y = self.bounds[1] + round((self.bounds[3] - IMAGE_SIZE) / 2)
    text_x = root_x + IMAGE_SIZE + 12
    max_line_width = self.bounds[2] - text_x
    text_gap = 25

    # Album image
    helpers.draw_divider(
      image_draw,
      root_x - 3,
      root_y - 3,
      IMAGE_SIZE + 5,
      IMAGE_SIZE + 5
    )
    if self.album_image != None:
      image.paste(self.album_image, (root_x, root_y))

    # Artist name
    helpers.draw_wrapped_text_lines(
      image_draw,
      self.track_data['artist_name'],
      fonts.KEEP_CALM_20,
      (text_x, root_y + 3),
      gap=text_gap,
      max_width=max_line_width,
      max_lines=1
    )

    # Track name
    helpers.draw_wrapped_text_lines(
      image_draw,
      self.track_data['track_name'],
      fonts.KEEP_CALM_24,
      (text_x, root_y + 27),
      gap=text_gap,
      max_width=max_line_width,
      max_lines=2
    )

    # Album name
    helpers.draw_wrapped_text_lines(
      image_draw,
      self.track_data['album_name'],
      fonts.KEEP_CALM_20,
      (text_x, root_y + 82),
      gap=text_gap,
      max_width=max_line_width,
      max_lines=1
    )
