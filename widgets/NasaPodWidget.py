import urllib
from PIL import Image
from io import BytesIO
from modules import fetch
from widgets.Widget import Widget
from modules.constants import WIDGET_BOUNDS_RIGHT

BOUNDS = WIDGET_BOUNDS_RIGHT

# URL of the main page
PAGE_URL = 'https://apod.nasa.gov/apod/astropix.html'

#
# NasaPodWidget class
#
class NasaPodWidget(Widget):
  #
  # Constructor
  #
  def __init__(self):
    super().__init__(BOUNDS)

    self.img_url = None
    self.image = None

  #
  # Update latest image
  #
  def update_data(self):
    self.img_url = None

    try:
      # Fetch NASA Picture of the Day
      page_lines = fetch.fetch_text(PAGE_URL).splitlines()
      for l in page_lines:
        # <IMG SRC="image/2209/Interval29seconds_Transit1200.jpg"
        if 'SRC' in l:
          src = l[10:-1]
          self.img_url = f"https://apod.nasa.gov/apod/{src}"
      print(f"[nasapod] {self.img_url}")

      # Page format changed?
      if not self.img_url:
        raise Exception('Failed to locate img src in page')

      # Download image
      img_data = urllib.request.urlopen(self.img_url).read()
      img = Image.open(BytesIO(img_data))

      # Resize, keeping aspect ratio
      max_height = BOUNDS[3]
      width, height = img.size
      ratio = width / height
      final_width = int(round(max_height * ratio, 0))
      print(f"[nasapod] resize {width}x{height} -> {final_width}x{max_height} r: {ratio}")
      self.image = img.resize((final_width, max_height)).convert('RGBA')
      print(f"[nasapod] Got image")

      self.unset_error()
    except Exception as err:
      self.set_error(err)

  #
  # Draw the image to fit
  #
  def draw_data(self, image_draw, image):
    root_x = self.bounds[0] + 5
    root_y = self.bounds[1] - 1

    # Image
    if self.image != None:
      image.paste(self.image, (root_x, root_y))