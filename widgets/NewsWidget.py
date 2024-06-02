from xml.dom import minidom
from datetime import datetime
from modules import fetch, helpers, images, fonts, config, log
from widgets.Widget import Widget

# Max number of displayed stories
MAX_STORIES = 5

config.require(['NEWS_CATEGORY', 'NEWS_MODE'])

#
# News widget class
#
class NewsWidget(Widget):
  #
  # Constructor
  #
  def __init__(self, bounds):
    super().__init__(bounds)

    # Validate NEWS_MODE
    news_mode = config.get('NEWS_MODE')
    if news_mode not in ['list', 'rotation']:
      raise Exception(f'Invaid NEWS_MODE {news_mode}')

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

      log.info('news', f"{len(self.stories)} stories")
      self.unset_error()
    except Exception as err:
      self.set_error(err)

  #
  # Draw news items as a list
  #
  def draw_list(self, image_draw, image):
    root_x = self.bounds[0]
    root_y = self.bounds[1] + 10
    story_gap = 60
    text_gap = 25
    font = fonts.KEEP_CALM_20
    icon_w_margin = 55
    story_x = root_x + icon_w_margin

    # Draw a list of icon-story items
    for story_index, story in enumerate(self.stories):
      story_y = root_y + (story_index * story_gap)
      max_line_width = self.bounds[2] - icon_w_margin - 20

      # Icon
      image.paste(images.ICON_NEWS, (root_x, story_y))

      # Wrapped lines
      lines = helpers.get_wrapped_lines(story['title'], font, max_line_width)[:2]
      for line_index, line in enumerate(lines):
        image_draw.text((story_x, story_y + 5 + (line_index * text_gap)), line, font = font, fill = 0)

  #
  # Draw news items as a rotation once a minute
  #
  def draw_rotation(self, image_draw, image):
    root_x = self.bounds[0]
    root_y = self.bounds[1] + 25
    icon_w_margin = 55
    max_line_width = self.bounds[2] - icon_w_margin - 20
    
    # Choose story
    now = datetime.now()
    story_index = now.hour % len(self.stories)
    story = self.stories[story_index]

    # Icon
    image.paste(images.ICON_NEWS, (root_x + 10, root_y - 5))
    
    # Title
    line_gap_y = 26
    font = fonts.KEEP_CALM_24
    lines = helpers.get_wrapped_lines(story['title'], font, max_line_width)
    for line_index, line in enumerate(lines):
      if line_index <= 3:
        image_draw.text((root_x + icon_w_margin + 10, root_y + (line_index * line_gap_y)), line, font = font, fill = 0)

    # Description
    desc_y = root_y + 90
    line_gap_y = 24
    font = fonts.KEEP_CALM_20
    lines = helpers.get_wrapped_lines(story['description'], font, max_line_width)
    for line_index, line in enumerate(lines):
      if line_index <= 10:
        image_draw.text((root_x + icon_w_margin + 10, desc_y + (line_index * line_gap_y)), line, font = font, fill = 0)
    
    # Story index
    bar_margin = 20
    bar_root_x = root_x + bar_margin
    box_gap = 25
    bar_len = (self.bounds[2] - (2 * bar_margin))
    total_gap = ((MAX_STORIES - 1) * box_gap)
    box_w = ((bar_len - total_gap) / MAX_STORIES)
    box_h = 8
    for index in range(0, MAX_STORIES):
      x = bar_root_x + (index * (box_w + box_gap))
      y = root_y + 262
      box_rhs = x + box_w
      box_bottom = y + box_h
      this_fill = 0 if index == story_index else 1
      image_draw.rectangle([x, y, box_rhs, box_bottom], fill = this_fill, outline = 0, width = 2)

  #
  # Draw the news stories
  #
  def draw_data(self, image_draw, image):
    news_mode = config.get('NEWS_MODE')

    if news_mode == 'list':
      self.draw_list(image_draw, image)
      return
    
    if news_mode == 'rotation':
      self.draw_rotation(image_draw, image)
      return
