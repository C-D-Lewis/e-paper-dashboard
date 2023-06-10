import os
import time
from datetime import datetime
from modules import fonts, helpers, epaper, timer, config
from widgets.WeatherWidget import WeatherWidget
from widgets.NewsWidget import NewsWidget
from widgets.TwitterWidget import TwitterWidget
from widgets.ForecastWidget import ForecastWidget
from widgets.QuotesWidget import QuotesWidget
from widgets.SpotifyWidget import SpotifyWidget
from widgets.NasaPodWidget import NasaPodWidget
from widgets.OnThisDayWidget import OnThisDayWidget
from modules.constants import DIVIDER_SIZE, WIDGET_BOUNDS_BOTTOM_LEFT, WIDGET_BOUNDS_RIGHT, WIDGET_BOUNDS_TOP, WIDGET_BOUNDS_TOP_LEFT, MIDWAY

# Top-right widget
TOP_RIGHT_WIDGET = WeatherWidget()
# Right rotation widgets and update intervals
RIGHT_WIDGETS = [
  { 'widget': NewsWidget(),     'interval': 60 },
  { 'widget': ForecastWidget(), 'interval': 60 },
  { 'widget': TwitterWidget(),  'interval': 30 },
  { 'widget': QuotesWidget(),   'interval': 15 },
  { 'widget': NasaPodWidget(),  'interval': 60 },
]
# Number of cycling widget pages
NUM_PAGES = len(RIGHT_WIDGETS)
# Left-top widget
LEFT_TOP_WIDGET = SpotifyWidget()
# Left-bottom widget
LEFT_BOTTOM_WIDGET = OnThisDayWidget()

config.require(['DRAW_DIVIDERS'])

################################### Drawing ####################################

#
# Draw time module
#
def draw_date_and_time(image_draw):
  root_x = 8
  root_y = 10

  now = datetime.now()
  time_str = now.strftime("%H:%M")
  image_draw.text((root_x, root_y), time_str, font = fonts.KEEP_CALM_80, fill = 0)
  date_str = now.strftime("%a %-d %b %Y")
  image_draw.text((root_x, root_y + 87), date_str, font = fonts.KEEP_CALM_46, fill = 0)

#
# Draw cycling page indicators
#
def draw_page_indicators(image_draw, page_index):
  root_x = MIDWAY + 20
  root_y = 268
  gap_y = 25
  size = 8
  border = 2

  # Prevent spill from left hand side
  bg_x = MIDWAY + 6
  bg_y = 167
  bg_width = 50
  image_draw.rectangle([bg_x, bg_y, bg_x + bg_width, bg_y + 313], fill = 1)

  # For each dot
  for index in range(0, NUM_PAGES):
    shape_y = root_y + (index * gap_y)

    # Draw outer edge
    outer_shape = (
      root_x - border,
      shape_y - border,
      root_x + size + border,
      shape_y + size + border
    )
    image_draw.ellipse(outer_shape, fill = 0)

    # Fill if the selected one
    selected = page_index == index
    fill = 0 if selected else 1
    image_draw.ellipse((root_x, shape_y, root_x + size, shape_y + size), fill = fill)

#
# Draw all dividers between widgets
#
def draw_dividers(image_draw):
  # Top from bottom
  helpers.draw_divider(
    image_draw,
    0,
    WIDGET_BOUNDS_TOP[3],
    WIDGET_BOUNDS_TOP[2],
    DIVIDER_SIZE
  )

  # Left 'half' top from bottom
  divider_2_y = WIDGET_BOUNDS_TOP[3] + DIVIDER_SIZE + WIDGET_BOUNDS_TOP_LEFT[3]
  helpers.draw_divider(
    image_draw,
    0,
    divider_2_y,
    MIDWAY,
    DIVIDER_SIZE
  )

  # Left 'half' from right 'half'
  divider_3_y = WIDGET_BOUNDS_TOP[3] + DIVIDER_SIZE
  helpers.draw_divider(
    image_draw,
    MIDWAY,
    divider_3_y,
    DIVIDER_SIZE,
    WIDGET_BOUNDS_RIGHT[3]
  )

#
# Draw all bounds for debugging purposes
#
def draw_all_bounds(image_draw):
  helpers.draw_divider(image_draw, *WIDGET_BOUNDS_TOP_LEFT)
  helpers.draw_divider(image_draw, *WIDGET_BOUNDS_BOTTOM_LEFT)
  helpers.draw_divider(image_draw, *WIDGET_BOUNDS_RIGHT)

################################## Main loop ###################################

#
# Draw things
#
def draw():
  timer.start()
  image, image_draw = epaper.prepare()

  # Top section
  draw_date_and_time(image_draw)
  TOP_RIGHT_WIDGET.draw(image_draw, image)
  LEFT_TOP_WIDGET.draw(image_draw, image)
  LEFT_BOTTOM_WIDGET.draw(image_draw, image)

  # Decorations
  if config.get('DRAW_DIVIDERS'):
    draw_dividers(image_draw)
  
  # Cycling widgets on the right side
  now = datetime.now()
  index = now.minute % NUM_PAGES
  draw_page_indicators(image_draw, index)
  RIGHT_WIDGETS[index]['widget'].draw(image_draw, image)

  # Help debug bounds issues
  # draw_all_bounds(image_draw)

  # Update display
  epaper.show(image)
  timer.end('main draw')
  time.sleep(2)

#
# Wait for the next minute
#
def wait_for_next_minute():
  now = datetime.now()
  while now.second != 1:
    now = datetime.now()
    time.sleep(1)

#
# The main function
#
def main():
  # Initial update and draw
  timer.start()
  TOP_RIGHT_WIDGET.update_data()
  LEFT_TOP_WIDGET.update_data()
  LEFT_BOTTOM_WIDGET.update_data()
  for item in RIGHT_WIDGETS:
    item['widget'].update_data()
  timer.end('initial update')
  epaper.init()
  draw()
  epaper.sleep()

  # Update once a minute forever
  while True:
    try:
      # Wait
      wait_for_next_minute()

      # Update data sources
      this_minute = datetime.now().minute
      updated = False
      timer.start()
      for item in RIGHT_WIDGETS:
        if this_minute % item['interval'] == 0:
          updated = True
          item['widget'].update_data()
      timer.end('main update')

      # Draw all widgets
      if updated:
        with helpers.timeout(seconds=45):
          epaper.init()
          draw()
          epaper.sleep()
      else:
        print('No widget updated, not refreshing e-paper')
    except TimeoutError as err:
      # Display lock, reboot the system
      os.system('sudo reboot')
    except Exception as err:
      # Failed to work normally
      print(err)
      time.sleep(5)

if __name__ in '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print('Exiting')
    epaper.deinit()
    exit()
