# Wrap text based on line length
# Adapted from https://itnext.io/how-to-wrap-text-on-image-using-python-8f569860f89e
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

# Get weekday name from index
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
