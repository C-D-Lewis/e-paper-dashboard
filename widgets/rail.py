from modules import fetch, images, helpers, fonts

MAX_WIDTH = 300

data = {
  'TfL Rail': 'Unknown',
  'Greater Anglia': 'Unknown'
}

# Get operator status from the page body fetched
def parse_operator_status(body, name):
  start = body.index(f"{name}</td>")
  temp = body[start:]
  start = temp.index('<td>') + len('<td>')
  temp = temp[start:]
  end = temp.index('</td>')
  return temp[:end]

# Fetch rail operator status
def fetch_status_page():
  url = 'http://www.nationalrail.co.uk/service_disruptions/indicator.aspx'
  return fetch.fetch_text(url, {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:88.0) Gecko/20100101 Firefox/88.0'
  })

# Fetch rail network delays status
def update_data():
  try:
    body = fetch_status_page()
    data['TfL Rail'] = parse_operator_status(body, 'TfL Rail')
    data['Greater Anglia'] = parse_operator_status(body, 'Greater Anglia')
    print(f"rail: {data}")
  except Exception as err:
    print('rail.update_data error: {0}'.format(err))
    data['TfL Rail'] = 'error'
    data['Greater Anglia'] = 'error'

# Draw rail statuses
def draw(canvas, image):
  root_x = 15
  text_x = 95
  text_gap = 25
  font = fonts.KEEP_CALM_28

  image.paste(images.ICON_TFL, (root_x, 175))
  lines = helpers.get_wrapped_lines(data['TfL Rail'], font, MAX_WIDTH)[:2]
  if len(lines) > 1:
    for index, line in enumerate(lines):
      canvas.text((text_x, 180 + (index * text_gap)), line, font = font, fill = 0)
  else:
    canvas.text((text_x, 194), data['TfL Rail'], font = font, fill = 0)

  image.paste(images.ICON_GA, (root_x, 239))
  lines = helpers.get_wrapped_lines(data['Greater Anglia'], font, MAX_WIDTH)[:2]
  if len(lines) > 1:
    for index, line in enumerate(lines):
      canvas.text((text_x, 240 + (index * text_gap)), line, font = font, fill = 0)
  else:
    canvas.text((text_x, 258), data['Greater Anglia'], font = font, fill = 0)
