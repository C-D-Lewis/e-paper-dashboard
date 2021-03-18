from xml.dom import minidom
from PIL import Image, ImageDraw, ImageOps
from io import BytesIO
import datetime
import urllib

from modules import fetch, fonts, config, helpers, images

MAX_WIDTH = 390
MAX_LINES = 7
IMAGE_SIZE = 64

data = {
  'id': '',
  'screen_name': '',
  'name': '',
  'image': None,
  'image_url': '',
  'tweet': {
    'text': '',
    'retweet_count': 0,
    'reply_count': 0,
    'like_count': 0,
    'quote_count': 0,
    'display_date': ''
  }
}

# Format the user's image to a circle
def format_image():
  # Create alpha mask for circular crop
  size = (IMAGE_SIZE, IMAGE_SIZE)
  mask = Image.new('L', size, 0)
  draw = ImageDraw.Draw(mask)
  draw.ellipse((0, 0) + size, fill=255)

  # Apply the mask
  output = ImageOps.fit(data['image'], mask.size, centering=(0.5, 0.5))
  output.putalpha(mask)

  background = Image.new('RGBA', size, (255,255,255))
  alpha_composite = Image.alpha_composite(background, output)
  data['image'] = alpha_composite

# Fill in error when API requests fail
def handle_api_error(err):
  print('twitter.update_data error: {0}'.format(err))
  data['id'] = 'error'
  data['name'] = 'error'
  data['image'] = None,
  data['image_url'] = 'error'
  data['tweet'] = {
    'text': 'error',
    'retweet_count': 0,
    'reply_count': 0,
    'like_count': 0,
    'quote_count': 0,
    'display_date': 'error'
  }

# Make an authenticated Twitter API request
def api_request(url):
  headers = {
    'Authorization': f"Bearer {config.get('TWITTER_BEARER_TOKEN')}"
  }
  return fetch.fetch_json(url, headers)

# Resolve the user ID from the screen name
def resolve_user_name():
  try:
    url = f"https://api.twitter.com/1.1/users/lookup.json?screen_name={config.get('TWITTER_SCREEN_NAME')}"
    json = api_request(url)

    user = json[0]
    data['screen_name'] = user['screen_name']
    data['name'] = user['name']
    data['id'] = user['id_str']
    data['image_url'] = user['profile_image_url_https'].replace('_normal', '')
  except Exception as err:
    handle_api_error(err)

# Update latest tweet
def update_data():
  try:
    url = f"https://api.twitter.com/2/users/{data['id']}/tweets?exclude=replies,retweets&tweet.fields=created_at,public_metrics"
    json = api_request(url)

    data['tweet'] = json['data'][0]

    # Test 280 length
    # data['tweet']['text'] = "This is a small change, but a big move for us. 140 was an arbitrary choice based on the 160 character SMS limit. Proud of how thoughtful the team has been in solving a real problem people have when trying to tweet. And at the same time maintaining our brevity, speed, and essence!"

    # Format datetime
    date_str = data['tweet']['created_at'].replace('Z', '')
    date_obj = datetime.datetime.fromisoformat(date_str)
    data['tweet']['display_date'] = date_obj.strftime("%H:%M %B %d, %Y")

    # Fetch image (it could change)
    img_data = urllib.request.urlopen(data['image_url']).read()
    data['image'] = Image.open(BytesIO(img_data)).resize((IMAGE_SIZE, IMAGE_SIZE)).convert('RGBA')
    format_image()

    print(f"twitter: {data}")
  except Exception as err:
    handle_api_error(err)

# Draw the news stories
def draw(canvas, image):
  root_x = 390
  root_y = 185
  line_gap_y = 23

  # Image
  # border = 2
  # canvas.ellipse((root_x - border, root_y - border, root_x + IMAGE_SIZE, root_y + IMAGE_SIZE), fill = 0)
  # canvas.ellipse((root_x, root_y, root_x + IMAGE_SIZE, root_y + IMAGE_SIZE), fill = 1)
  if data['image'] != None:
    image.paste(data['image'], (root_x, root_y))

  # Screen name, name and date
  content_x = root_x + IMAGE_SIZE + 10
  canvas.text((content_x, root_y + 10), data['name'], font = fonts.KEEP_CALM_24, fill = 0)
  canvas.text((content_x, root_y + 40), f"@{data['screen_name']}", font = fonts.KEEP_CALM_20, fill = 0)

  # Tweet content, wrapped
  content = data['tweet']['text']
  content_x = root_x
  paragraph_y = root_y + 75
  lines = helpers.get_wrapped_lines(content, fonts.KEEP_CALM_20, MAX_WIDTH)
  font = fonts.KEEP_CALM_18 if len(lines) > MAX_LINES else fonts.KEEP_CALM_20
  for index, line in enumerate(lines):
    canvas.text((content_x, paragraph_y + (index * line_gap_y)), line, font = font, fill = 0)

  # Footer, after text
  paragraph_height = helpers.get_paragraph_height(content, font, MAX_WIDTH, line_gap_y)
  line_y = paragraph_y + paragraph_height + 5
  helpers.draw_divider(canvas, root_x, line_y, 380, 1)

  # Tweet stats
  stats_y = line_y + 10
  image.paste(images.ICON_HEART, (root_x + 10, stats_y - 3))
  likes_str = helpers.format_number(data['tweet']['public_metrics']['like_count'])
  canvas.text((root_x + 40, stats_y), likes_str, font = fonts.KEEP_CALM_18, fill = 0)
  image.paste(images.ICON_SPEECH, (root_x + 95, stats_y - 1))
  reply_str = helpers.format_number(data['tweet']['public_metrics']['reply_count'])
  canvas.text((root_x + 127, stats_y), reply_str, font = fonts.KEEP_CALM_18, fill = 0)

  # Tweet date
  date_x = content_x + IMAGE_SIZE + 120
  canvas.text((date_x, stats_y), f"{data['tweet']['display_date']}", font = fonts.KEEP_CALM_18, fill = 0)
