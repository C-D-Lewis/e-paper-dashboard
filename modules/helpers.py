import signal

#
# Wrap text based on line length
#   Adapted from https://itnext.io/how-to-wrap-text-on-image-using-python-8f569860f89e
#
def get_wrapped_lines(text, font, max_width):
  lines = []

  words = text.split(' ')
  i = 0
  while i < len(words):
    line = ''
    while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
      line = line + words[i]+ " "
      i += 1
    if not line:
      line = words[i]
      i += 1
    lines.append(line)
  return lines

#
# Get the height of a paragraph of text
#
def get_paragraph_height(text, font, max_width, gap_y):
  lines = get_wrapped_lines(text, font, max_width)
  return (len(lines) + 1) * gap_y

#
# Get weekday name from index
#
def get_weekday_name(index):
  if index == 0:
    return 'Monday'
  if index == 1:
    return 'Tuesday'
  if index == 2:
    return 'Wednesday'
  if index == 3:
    return 'Thursday'
  if index == 4:
    return 'Friday'
  if index == 5:
    return 'Saturday'
  return 'Sunday'

#
# Draw a divider rect
#
def draw_divider(image_draw, x, y, w, h, grey = False):
  rect_w = x + w
  rect_h = y + h

  # Black rect
  image_draw.rectangle([x, y, rect_w, rect_h], fill = 0)

  # TODO: Grey with alternating white (orientations?)
  if grey:
    cursor_x = x
    cursor_y = y
    # For each x
    while cursor_x < cursor_x + rect_w:
      fill = 0



#
# Format a number e.g: 1342 to 1.3k
#
def format_number(val):
  if val > 1000000:
    return f"{round(val / 1000000, 1)}M"
  if val > 1000:
    return f"{round(val / 1000, 1)}K"
  return f"{val}"

#
# Draw a limited number of wrapped lines of text
#
def draw_wrapped_text_lines(image_draw, str, font, root_xy, gap, max_width, max_lines):
  text_x = root_xy[0]
  text_y = root_xy[1]
  lines = get_wrapped_lines(str, font, max_width)[:max_lines]
  if len(lines) > 1:
    for index, line in enumerate(lines):
      image_draw.text((text_x, text_y + 5 + (index * gap)), line, font = font, fill = 0)
  else:
    image_draw.text((text_x, text_y + 5), str, font = font, fill = 0)

#
# Timeout class
#   https://stackoverflow.com/a/22348885
#
class timeout:
  def __init__(self, seconds=1, error_message='Timeout'):
    self.seconds = seconds
    self.error_message = error_message
  def handle_timeout(self, signum, frame):
    raise TimeoutError(self.error_message)
  def __enter__(self):
    signal.signal(signal.SIGALRM, self.handle_timeout)
    signal.alarm(self.seconds)
  def __exit__(self, type, value, traceback):
    signal.alarm(0)
