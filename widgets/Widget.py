from modules import fonts

#
# Widget base class
#
class Widget:
  #
  # Constructor
  #
  def __init__(self, bounds):
    self.bounds = bounds
    self.error = None

  #
  # Set an error encountered
  #
  def set_error(self, err):
    print(err)
    self.error = err

  #
  # Clear the error state
  #
  def unset_error(self):
    self.error = None

  #
  # Update data method, to be overridden
  #
  def update_data(self):
    pass

  #
  # Clear to prevent overlap (but must still draw from left to right)
  #
  def clear(self, image_draw):
    x = self.bounds[0]
    y = self.bounds[1]
    w = self.bounds[2]
    h = self.bounds[3]
    image_draw.rectangle([x, y, x + w, y + h], fill = 1)

  #
  # Base draw method that handles drawing error and user draw
  #
  def draw(self, image_draw, image):
    self.clear(image_draw)

    # Draw any set error
    if self.error:
      self.draw_error(image_draw)
      return

    # Try and draw
    try:
      self.draw_data(image_draw, image)
    except Exception as err:
      self.set_error(err)
      self.draw_error(image_draw)

  #
  # Draw error message
  #
  def draw_error(self, image_draw):
    image_draw.text((self.bounds[0], self.bounds[1]), f"{self.error}", font = fonts.KEEP_CALM_20, fill = 0)

  #
  # Base draw method, to be overridden
  #
  def draw_data(self, image_draw, image):
    raise Exception('Draw not implemented for one or more widgets')
