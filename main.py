import time
from datetime import datetime

from modules import fonts, config, helpers, epaper
from widgets import weather, rail, news, crypto, twitter

# Constants
UPDATE_INTERVAL_M = 15
NUM_PAGES = 3

################################### Drawing ####################################

# Draw time module
def draw_date_and_time(image_draw):
  root_x = 10
  root_y = 10

  now = datetime.now()
  time_str = now.strftime("%H:%M")
  image_draw.text((root_x, root_y), time_str, font = fonts.KEEP_CALM_80, fill = 0)
  date_str = now.strftime("%B %d, %Y")
  image_draw.text((root_x, root_y + 85), date_str, font = fonts.KEEP_CALM_48, fill = 0)

# Draw cycling page indicators
def draw_page_indicators(image_draw, page_index):
  root_x = 370
  root_y = 290
  gap_y = 25
  size = 8
  border = 2

  for index in range(0, NUM_PAGES):
    shape_y = root_y + (index * gap_y)

    outer_shape = (root_x - border, shape_y - border, root_x + size + border, shape_y + size + border)
    image_draw.ellipse(outer_shape, fill = 0)

    selected = page_index == index
    fill = 0 if selected else 1
    image_draw.ellipse((root_x, shape_y, root_x + size, shape_y + size), fill = fill)

################################## Main loop ###################################

# Draw things
def draw():
  # Prepare
  image, image_draw = epaper.prepare()

  # Draw content
  draw_date_and_time(image_draw)
  weather.draw(image_draw, image)
  rail.draw(image_draw, image)
  crypto.draw(image_draw, image)
  helpers.draw_divider(image_draw, 0, 160, image.width, 5)
  helpers.draw_divider(image_draw, 0, 310, 350, 5)
  helpers.draw_divider(image_draw, 350, 165, 5, 320)

  # Cycling pages
  now = datetime.now()
  index = now.minute % NUM_PAGES
  if index == 0:
    news.draw(image_draw, image)
  elif index == 1:
    weather.draw_forecast(image_draw, image)
  elif index == 2:
    twitter.draw(image_draw, image)
  else:
    print(f"! Unused page index {index}")
  draw_page_indicators(image_draw, index)

  # Update display
  epaper.show(image)
  time.sleep(2)

# Update all data sources
def update_data_sources():
  weather.update_data()
  rail.update_data()
  crypto.update_data()
  news.update_data()
  twitter.update_data()

# Update all the things
def update():
  if datetime.now().minute % UPDATE_INTERVAL_M == 0:
    update_data_sources()

# Wait for the next minute
def wait_for_next_minute():
  now = datetime.now()
  while now.second != 1:
    now = datetime.now()
    time.sleep(0.4)

# The main function
def main():
  config.load()
  twitter.resolve_user_name()

  # Initial update
  update_data_sources()

  # Update once a minute
  while True:
    update()
    epaper.init()
    draw()
    epaper.sleep()
    wait_for_next_minute()

if __name__ in '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print('Exiting')
    epaper.deinit()
    exit()
