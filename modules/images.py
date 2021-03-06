import os
from PIL import Image

IMAGES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../images')

ICON_CLOUD_DAY = Image.open(os.path.join(IMAGES_DIR, 'cloud.bmp'))
ICON_CLOUD_NIGHT = Image.open(os.path.join(IMAGES_DIR, 'cloud-night.bmp'))
ICON_WIND = Image.open(os.path.join(IMAGES_DIR, 'wind.bmp'))
ICON_RAIN = Image.open(os.path.join(IMAGES_DIR, 'rain.bmp'))
ICON_RAIN_32 = Image.open(os.path.join(IMAGES_DIR, 'rain_32.bmp'))
ICON_CLEAR_DAY = Image.open(os.path.join(IMAGES_DIR, 'sun.bmp'))
ICON_CLEAR_NIGHT = Image.open(os.path.join(IMAGES_DIR, 'moon.bmp'))
ICON_STORM = Image.open(os.path.join(IMAGES_DIR, 'storm.bmp'))
ICON_SNOW = Image.open(os.path.join(IMAGES_DIR, 'snow.bmp'))
ICON_FROST = Image.open(os.path.join(IMAGES_DIR, 'frost.bmp'))
ICON_FOG = Image.open(os.path.join(IMAGES_DIR, 'fog.bmp'))

ICON_TFL = Image.open(os.path.join(IMAGES_DIR, 'tfl.bmp'))
ICON_GA = Image.open(os.path.join(IMAGES_DIR, 'ga.bmp'))

ICON_BTC = Image.open(os.path.join(IMAGES_DIR, 'btc.bmp'))
ICON_ETH = Image.open(os.path.join(IMAGES_DIR, 'eth.bmp'))

ICON_NEWS = Image.open(os.path.join(IMAGES_DIR, 'news.bmp'))

ICON_ERROR = Image.open(os.path.join(IMAGES_DIR, 'error.bmp'))
ICON_QUESTION_MARK = Image.open(os.path.join(IMAGES_DIR, 'question.bmp'))
