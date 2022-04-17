from modules import fonts

#
# Widget class
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
  # Draw error message
  #
  def draw_error(self, image_draw):
    image_draw.text((self.bounds[0], self.bounds[1]), f"{self.error}", font = fonts.KEEP_CALM_20, fill = 0)

  #
  # Base draw method, to be overridden
  #
  def draw(self, image_draw, image):
    raise Exception('Draw not implemented for one or more widgets')
