# E-paper width
IMAGE_WIDTH = 800

# E-paper height
IMAGE_HEIGHT = 480

# Midway between the left and right half
MIDWAY = 380

# Size of middle divider
DIVIDER_SIZE = 5

# Width of paged dots section
DOTS_SIZE = 35

# Top banner
WIDGET_BOUNDS_TOP = (0, 0, IMAGE_WIDTH, 160)

# Top left slot
WIDGET_BOUNDS_LEFT_TOP = (0, 165, MIDWAY, 154)

# Bottom left slot
WIDGET_BOUNDS_LEFT_BOTTOM = (0, 325, MIDWAY, 154)

# Right 'half' slot
WIDGET_BOUNDS_RIGHT = (
  MIDWAY + DIVIDER_SIZE + DOTS_SIZE,
  WIDGET_BOUNDS_TOP[3] + DIVIDER_SIZE + 2,
  MIDWAY,
  315
)

# Left 'half' slot
WIDGET_BOUNDS_LEFT = (
  WIDGET_BOUNDS_LEFT_TOP[0],
  WIDGET_BOUNDS_LEFT_TOP[1],
  MIDWAY,
  WIDGET_BOUNDS_LEFT_TOP[3] + WIDGET_BOUNDS_LEFT_BOTTOM[3]
)

# Hour the day starts
DAY_START_HOUR = 6

# Hour the day ends
DAY_END_HOUR = 18

# Miles per hour per 1 kph
MPH_PER_KPH = 0.621371
