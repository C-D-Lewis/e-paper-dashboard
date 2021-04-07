from modules import fonts

# Widget class
class Widget:
  # Constructor
  def __init__(self, bounds):
    self.bounds = bounds
    self.error = None

  # Set an error encountered
  def set_error(self, err):
    print(err)
    self.error = err

  # Clear the error state
  def unset_error(self):
    self.error = None

  # Update data method
  def update_data(self):
    pass

  # Draw error message
  def draw_error(self, image_draw):
    image_draw.text((self.bounds[0], self.bounds[1]), f"{self.error}", font = fonts.KEEP_CALM_20, fill = 0)

  # Base draw method
  def draw(self, image_draw, image):
    image_draw.text((self.bounds[0], self.bounds[1]), "draw not implemented", font = fonts.KEEP_CALM_20, fill = 0)
