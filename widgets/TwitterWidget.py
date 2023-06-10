import datetime
import urllib
from PIL import Image, ImageDraw, ImageOps
from io import BytesIO
from modules import fetch, fonts, config, helpers, images, log
from widgets.Widget import Widget
from modules.constants import WIDGET_BOUNDS_RIGHT

BOUNDS = WIDGET_BOUNDS_RIGHT

# Max lines to display
MAX_LINES = 7
# Image icon size
IMAGE_SIZE = 64

config.require(['TWITTER_BEARER_TOKEN', 'TWITTER_SCREEN_NAME'])

#
# Make an authenticated Twitter API request
#
def api_request(url):
  headers = { 'Authorization': f"Bearer {config.get('TWITTER_BEARER_TOKEN')}" }
  return fetch.fetch_json(url, headers)

#
# TwitterWidget class
#
class TwitterWidget(Widget):
  #
  # Constructor
  #
  def __init__(self):
    super().__init__(BOUNDS)

    self.id = ''
    self.screen_name = ''
    self.name = ''
    self.image = None
    self.image_url = ''
    self.tweet = {
      'text': '',
      'retweet_count': 0,
      'reply_count': 0,
      'like_count': 0,
      'quote_count': 0,
      'display_date': ''
    }

    # Initial data
    self.resolve_user_name()

  #
  # Format the user's image to a circle
  #
  def convert_image(self):
    # Create alpha mask for circular crop
    size = (IMAGE_SIZE, IMAGE_SIZE)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)

    # Apply the mask
    output = ImageOps.fit(self.image, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    # Flatten alpha to remove outer pixels
    background = Image.new('RGBA', size, (255,255,255))
    alpha_composite = Image.alpha_composite(background, output)
    self.image = alpha_composite

  #
  # Resolve the user ID from the screen name
  #
  def resolve_user_name(self):
    try:
      url = f"https://api.twitter.com/1.1/users/lookup.json?screen_name={config.get('TWITTER_SCREEN_NAME')}"
      json = api_request(url)

      user = json[0]
      self.screen_name = user['screen_name']
      self.name = user['name']
      self.id = user['id_str']
      self.image_url = user['profile_image_url_https'].replace('_normal', '')
    except Exception as err:
      self.set_error(err)

  # Update latest tweet
  def update_data(self):
    try:
      # Check ID fetch didn't fail
      if self.id == '':
        self.resolve_user_name()

      # Get user's tweets
      url = f"https://api.twitter.com/2/users/{self.id}/tweets?exclude=replies,retweets&tweet.fields=created_at,public_metrics"
      json = api_request(url)
      self.tweet = json['data'][0]

      # Test 280 length
      # self.tweet['text'] = "This is a small change, but a big move for us. 140 was an arbitrary choice based on the 160 character SMS limit. Proud of how thoughtful the team has been in solving a real problem people have when trying to tweet. And at the same time maintaining our brevity, speed, and essence!"

      # Format datetime
      date_str = self.tweet['created_at'].replace('Z', '')
      date_obj = datetime.datetime.fromisoformat(date_str)
      self.tweet['display_date'] = date_obj.strftime("%H:%M %b %d, %Y")

      # Fetch image (it could change)
      img_data = urllib.request.urlopen(self.image_url).read()
      self.image = Image.open(BytesIO(img_data)).resize((IMAGE_SIZE, IMAGE_SIZE)).convert('RGBA')
      self.convert_image()

      log.info('twitter', self.tweet)
      self.unset_error()
    except Exception as err:
      self.set_error(err)

  # Draw the tweet
  def draw_data(self, image_draw, image):
    root_x = self.bounds[0] + 5
    root_y = self.bounds[1] + 10
    line_gap_y = 25
    max_line_width = self.bounds[2] - 10

    # Image
    if self.image != None:
      image.paste(self.image, (root_x, root_y))

    # Screen name, name and date
    content_x = root_x + IMAGE_SIZE + 10
    image_draw.text((content_x, root_y + 10), self.name, font = fonts.KEEP_CALM_24, fill = 0)
    image_draw.text((content_x, root_y + 40), f"@{self.screen_name}", font = fonts.KEEP_CALM_20, fill = 0)

    # Tweet content, wrapped
    content = self.tweet['text']
    content_x = root_x
    paragraph_y = root_y + 75
    lines = helpers.get_wrapped_lines(content, fonts.KEEP_CALM_20, max_line_width)
    font = fonts.KEEP_CALM_18 if len(lines) > MAX_LINES else fonts.KEEP_CALM_20
    lines = helpers.get_wrapped_lines(content, font, max_line_width)
    for index, line in enumerate(lines):
      image_draw.text((content_x, paragraph_y + (index * line_gap_y)), line, font = font, fill = 0)

    # Footer, after text
    paragraph_height = helpers.get_paragraph_height(content, font, max_line_width, line_gap_y)
    line_y = paragraph_y + paragraph_height + 5
    helpers.draw_divider(image_draw, root_x, line_y, 370, 1)

    # Tweet stats
    stats_y = line_y + 10
    font = fonts.KEEP_CALM_18
    image.paste(images.ICON_HEART, (root_x + 5, stats_y - 3))
    likes_str = helpers.format_number(self.tweet['public_metrics']['like_count'])
    image_draw.text((root_x + 35, stats_y), likes_str, font = font, fill = 0)
    image.paste(images.ICON_RETWEET, (root_x + 90, stats_y - 4))
    retweet_str = helpers.format_number(self.tweet['public_metrics']['retweet_count'])
    image_draw.text((root_x + 117, stats_y), retweet_str, font = font, fill = 0)

    # Tweet date
    date_x = content_x + IMAGE_SIZE + 110
    image_draw.text((date_x, stats_y), f"{self.tweet['display_date']}", font = font, fill = 0)
