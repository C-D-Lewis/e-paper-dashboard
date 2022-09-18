import urllib
from PIL import Image
from io import BytesIO
from modules import fetch, fonts
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
    self.description = None

    try:
      # Fetch NASA Picture of the Day
      page_lines = fetch.fetch_text(PAGE_URL).splitlines()
      for l in page_lines:
        # <IMG SRC="image/2209/Interval29seconds_Transit1200.jpg"
        if 'SRC' in l:
          src = l.split('"')[1]
          self.img_url = f"https://apod.nasa.gov/apod/{src}"
        # <b> Sea and Sky Glows over the Oregon Coast </b> <br>
        # <b>North America and the Pelican</b> <br>
        if '</b> <br>' in l and not self.description:
          self.description = l.split('<b>')[1].split('</b>')[0].strip()
      print(f"[nasapod] {self.img_url}")
      print(f"[nasapod] {self.description}")

      # Page format changed?
      if not self.img_url:
        raise Exception('Failed to locate img src in page')

      # Download image
      img_data = urllib.request.urlopen(self.img_url).read()
      img = Image.open(BytesIO(img_data))

      # Resize, keeping aspect ratio
      max_height = self.bounds[3] - 40
      width, height = img.size
      ratio = width / height
      final_width = int(round(max_height * ratio, 0))
      print(f"[nasapod] resize {width}x{height} -> {final_width}x{max_height} r: {ratio}")
      self.image = img.resize((final_width, max_height)).convert('RGBA')
      self.image_width = final_width
      print(f"[nasapod] Got image")

      self.unset_error()
    except Exception as err:
      self.set_error(err)

  #
  # Draw the image to fit
  #
  def draw_data(self, image_draw, image):
    # Could be wider than the widget
    root_x = max(self.bounds[0], self.bounds[0] + int(round((self.bounds[2] - self.image_width) / 2)))
    root_y = self.bounds[1] + 5

    # Image
    if self.image != None:
      image.paste(self.image, (root_x, root_y))

    # Description
    text_x = self.bounds[0] + 5
    text_y = self.bounds[1] + self.bounds[3] - 28
    font = fonts.KEEP_CALM_18
    image_draw.text((text_x, text_y), self.description, font = font, fill = 0)
