from modules import fetch, images, helpers, fonts

RAIL_MAX_WIDTH = 320

rail_data = {}

# Fetch rail operator status
def fetch_operator_status(operator_name):
  url = 'http://www.nationalrail.co.uk/service_disruptions/indicator.aspx'
  body = fetch.fetch_text(url)
  start = body.index(f"{operator_name}</td>")
  temp = body[start:]
  start = temp.index('<td>') + 4
  temp = temp[start:]
  end = temp.index('</td>')
  return temp[:end]

# Fetch rail network delays status
def update_data():
  try:
    rail_data['TfL Rail'] = fetch_operator_status('TfL Rail')
    rail_data['Greater Anglia'] = fetch_operator_status('Greater Anglia')
    print(f"rail: {rail_data}")
  except Exception as err:
    print('rail.update_data error: {0}'.format(err))
    rail_data['TfL Rail'] = 'error'
    rail_data['Greater Anglia'] = 'error'

# Draw rail statuses
def draw(canvas, image):
  image.paste(images.ICON_TFL, (15, 175))
  lines = helpers.get_wrapped_lines(rail_data['TfL Rail'], fonts.KEEP_CALM_28, RAIL_MAX_WIDTH)[:2]
  if len(lines) > 1:
    for index, line in enumerate(lines):
      canvas.text((95, 180 + (index * 25)), line, font = fonts.KEEP_CALM_28, fill = 0)
  else:
    canvas.text((95, 191), rail_data['TfL Rail'], font = fonts.KEEP_CALM_28, fill = 0)

  image.paste(images.ICON_GA, (15, 239))
  lines = helpers.get_wrapped_lines(rail_data['Greater Anglia'], fonts.KEEP_CALM_28, RAIL_MAX_WIDTH)[:2]
  if len(lines) > 1:
    for index, line in enumerate(lines):
      canvas.text((95, 240 + (index * 25)), line, font = fonts.KEEP_CALM_28, fill = 0)
  else:
    canvas.text((95, 255), rail_data['Greater Anglia'], font = fonts.KEEP_CALM_28, fill = 0)
