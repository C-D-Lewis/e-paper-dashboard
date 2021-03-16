from xml.dom import minidom
import datetime

from modules import fetch, fonts, config

MAX_WIDTH = 360

data = {
  'id': '',
  'screen_name': '',
  'image': '',
  'name': '',
  'content': '',
  'date': ''
}

# Fill in error when API requests fail
def handle_api_error(err):
  print('twitter.update_data error: {0}'.format(err))
  data['id'] = 'error'
  data['name'] = 'error'
  data['image'] = 'error'
  data['content'] = 'error'
  data['date'] = 'error'

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
    data['image'] = user['profile_image_url_https'].replace('_normal', '')
  except Exception as err:
    handle_api_error(err)

# Update latest tweet
def update_data():
  try:
    url = f"https://api.twitter.com/2/users/{data['id']}/tweets?exclude=replies,retweets&tweet.fields=created_at"
    json = api_request(url)

    tweet = json['data'][0]
    data['content'] = tweet['text']

    # Format datetime
    date_str = tweet['created_at'].replace('Z', '')
    date_obj = datetime.datetime.fromisoformat(date_str)
    data['date'] = date_obj.strftime("%H:%M, %B %d, %Y")

    print(f"twitter: {data}")
  except Exception as err:
    handle_api_error(err)

# Draw the news stories
def draw(canvas, image):
  canvas.text((400, 200), "twitter!", font = fonts.KEEP_CALM_20, fill = 0)
