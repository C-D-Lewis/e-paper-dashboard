from xml.dom import minidom

from modules import fetch, helpers, images, fonts, config

MAX_STORIES = 5
MAX_WIDTH = 360

data = { 'stories': [] }

# Update news stories
def update_data():
  try:
    url = f"http://feeds.bbci.co.uk/news/{config.get('NEWS_CATEGORY')}/rss.xml"
    text = fetch.fetch_text(url)

    data['stories'] = []
    xml = minidom.parseString(text)
    items = xml.getElementsByTagName('item')[:MAX_STORIES]

    for item in items:
      data['stories'].append({
        'title': item.getElementsByTagName('title')[0].firstChild.data,
        'description': item.getElementsByTagName('description')[0].firstChild.data,
        'pubdate': item.getElementsByTagName('pubDate')[0].firstChild.data
      })
    print(f"news: {len(data['stories'])} stories")
  except Exception as err:
    print('news.update_data error: {0}'.format(err))
    data['stories'] = [{
      'title': 'error',
      'description': 'error',
      'pubdate': 'error'
    }]

# Draw the news stories
def draw(canvas, image):
  root_x = 390
  root_y = 180
  story_gap = 60
  text_gap = 25
  font = fonts.KEEP_CALM_20

  stories = data['stories']
  for story_index, story in enumerate(stories):
    story_y = root_y + (story_index * story_gap)

    image.paste(images.ICON_NEWS, (root_x, story_y))

    lines = helpers.get_wrapped_lines(story['title'], font, MAX_WIDTH)[:2]
    for line_index, line in enumerate(lines):
      canvas.text((root_x + 55, story_y + 5 + (line_index * text_gap)), line, font = font, fill = 0)
