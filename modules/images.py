import os
from PIL import Image

IMAGES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../images')

# Weather
ICON_CLOUD_DAY = Image.open(os.path.join(IMAGES_DIR, 'cloud.bmp'))
ICON_CLOUD_NIGHT = Image.open(os.path.join(IMAGES_DIR, 'cloud-night.bmp'))
ICON_WIND = Image.open(os.path.join(IMAGES_DIR, 'wind.bmp'))
ICON_RAIN = Image.open(os.path.join(IMAGES_DIR, 'rain.bmp'))
ICON_CLEAR_DAY = Image.open(os.path.join(IMAGES_DIR, 'sun.bmp'))
ICON_CLEAR_NIGHT = Image.open(os.path.join(IMAGES_DIR, 'moon.bmp'))
ICON_STORM = Image.open(os.path.join(IMAGES_DIR, 'storm.bmp'))
ICON_SNOW = Image.open(os.path.join(IMAGES_DIR, 'snow.bmp'))
ICON_FROST = Image.open(os.path.join(IMAGES_DIR, 'frost.bmp'))
ICON_FOG = Image.open(os.path.join(IMAGES_DIR, 'fog.bmp'))
ICON_RAIN_32 = Image.open(os.path.join(IMAGES_DIR, 'rain_32.bmp'))
ICON_WINDSOCK_32 = Image.open(os.path.join(IMAGES_DIR, 'windsock.bmp'))

# Weather forecast
ICON_CLOUD_DAY_48 = Image.open(os.path.join(IMAGES_DIR, 'cloud_48.bmp'))
ICON_CLOUD_NIGHT_48 = Image.open(os.path.join(IMAGES_DIR, 'cloud-night_48.bmp'))
ICON_RAIN_48 = Image.open(os.path.join(IMAGES_DIR, 'rain_48.bmp'))
ICON_CLEAR_DAY_48 = Image.open(os.path.join(IMAGES_DIR, 'sun_48.bmp'))
ICON_CLEAR_NIGHT_48 = Image.open(os.path.join(IMAGES_DIR, 'moon_48.bmp'))
ICON_STORM_48 = Image.open(os.path.join(IMAGES_DIR, 'storm_48.bmp'))
ICON_SNOW_48 = Image.open(os.path.join(IMAGES_DIR, 'snow_48.bmp'))
ICON_FROST_48 = Image.open(os.path.join(IMAGES_DIR, 'frost_48.bmp'))
ICON_FOG_48 = Image.open(os.path.join(IMAGES_DIR, 'fog_48.bmp'))

# Rail
ICON_TFL = Image.open(os.path.join(IMAGES_DIR, 'tfl.bmp'))
ICON_GA = Image.open(os.path.join(IMAGES_DIR, 'ga.bmp'))

# Crypto
ICON_BTC = Image.open(os.path.join(IMAGES_DIR, 'btc.bmp'))
ICON_ETH = Image.open(os.path.join(IMAGES_DIR, 'eth.bmp'))

# News
ICON_NEWS = Image.open(os.path.join(IMAGES_DIR, 'news.bmp'))

# Twitter
ICON_HEART = Image.open(os.path.join(IMAGES_DIR, 'heart.bmp'))
ICON_SPEECH = Image.open(os.path.join(IMAGES_DIR, 'speech.bmp'))

# Other
ICON_ERROR = Image.open(os.path.join(IMAGES_DIR, 'error.bmp'))
ICON_QUESTION_MARK = Image.open(os.path.join(IMAGES_DIR, 'question.bmp'))