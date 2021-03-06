from xml.dom import minidom

from modules import fetch, helpers, images, fonts, config

NEWS_MAX_STORIES = 5
NEWS_MAX_WIDTH = 360

data = { 'stories': [] }

# Update news stories
def update_data():
  try:
    url = f"http://feeds.bbci.co.uk/news/{config.get('NEWS_CATEGORY')}/rss.xml"
    res = fetch.fetch_text(url)

    data['stories'] = []
    xml = minidom.parseString(res)
    items = xml.getElementsByTagName('item')[:NEWS_MAX_STORIES]

    for item in items:
      data['stories'].append({
        'title': item.getElementsByTagName('title')[0].firstChild.data,
        'description': item.getElementsByTagName('description')[0].firstChild.data,
        'pubdate': item.getElementsByTagName('pubDate')[0].firstChild.data
      })
    print(f"news: {len(data['stories'])} stories")
  except Exception as err:
    print('update_news_data error: {0}'.format(err))
    data['stories'] = [{
      'title': 'error',
      'description': 'error',
      'pubdate': 'error'
    }]

# Draw the news stories
def draw(canvas, image):
  root_x = 375
  root_y = 180
  gap_y = 60

  stories = data['stories']
  for story in stories:
    image.paste(images.ICON_NEWS, (root_x, root_y))
    lines = helpers.get_wrapped_lines(story['title'], fonts.KEEP_CALM_20, NEWS_MAX_WIDTH)[:2]
    for index, line in enumerate(lines):
      canvas.text((root_x + 55, root_y + 5 + (index * 25)), line, font = fonts.KEEP_CALM_20, fill = 0)

    root_y += gap_y
