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
def draw_divider(image_draw, x, y, w, h):
  image_draw.rectangle([x, y, x + w, y + h], fill = 0)

#
# Format a number e.g: 1342 to 1.3k
#
def format_number(val):
  if val > 1000000:
    return f"{round(val / 1000000, 1)}M"
  if val > 1000:
    return f"{round(val / 1000, 1)}K"
  return f"{val}"
