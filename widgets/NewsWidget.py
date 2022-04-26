from xml.dom import minidom
from modules import fetch, helpers, images, fonts, config
from widgets.Widget import Widget
from modules.constants import WIDGET_BOUNDS

NEWS_BOUNDS = WIDGET_BOUNDS[2]
# Max number of displayed stories
MAX_STORIES = 5

#
# News widget class
#
class NewsWidget(Widget):
  #
  # Constructor
  #
  def __init__(self):
    super().__init__(NEWS_BOUNDS)

    self.stories = []

  #
  # Update news stories
  #
  def update_data(self):
    try:
      # Fetch data
      url = f"http://feeds.bbci.co.uk/news/{config.get('NEWS_CATEGORY')}/rss.xml"
      text = fetch.fetch_text(url)

      # Parse
      self.stories = []
      xml = minidom.parseString(text)
      items = xml.getElementsByTagName('item')[:MAX_STORIES]
      for item in items:
        self.stories.append({
          'title': item.getElementsByTagName('title')[0].firstChild.data,
          'description': item.getElementsByTagName('description')[0].firstChild.data,
          'pubdate': item.getElementsByTagName('pubDate')[0].firstChild.data
        })

      print(f"[news] {len(self.stories)} stories")
      self.unset_error()
    except Exception as err:
      self.set_error(err)

  #
  # Draw the news stories
  #
  def draw_data(self, image_draw, image):
    story_gap = 60
    text_gap = 25
    font = fonts.KEEP_CALM_20
    left_margin = 55
    story_x = self.bounds[0] + left_margin

    # Draw a list of icon-story items
    for story_index, story in enumerate(self.stories):
      story_y = self.bounds[1] + (story_index * story_gap)
      max_line_width = self.bounds[2] - left_margin

      # Icon
      image.paste(images.ICON_NEWS, (self.bounds[0], story_y))

      # Wrapped lines
      lines = helpers.get_wrapped_lines(story['title'], font, max_line_width)[:2]
      for line_index, line in enumerate(lines):
        image_draw.text((story_x, story_y + 5 + (line_index * text_gap)), line, font = font, fill = 0)
