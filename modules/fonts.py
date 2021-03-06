import os
from PIL import ImageFont

FONTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../fonts')
FONT_PATH = os.path.join(FONTS_DIR, 'KeepCalm-Medium.ttf')

KEEP_CALM_20 = ImageFont.truetype(FONT_PATH, 20)
KEEP_CALM_28 = ImageFont.truetype(FONT_PATH, 28)
KEEP_CALM_48 = ImageFont.truetype(FONT_PATH, 48)
KEEP_CALM_80 = ImageFont.truetype(FONT_PATH, 80)
