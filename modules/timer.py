import time
from modules import log

start_time = 0

#
# Get current time
# - https://stackoverflow.com/a/5998359
#
def current_milli_time():
  return round(time.time() * 1000)

#
# Start the time
#
def start():
  global start_time

  start_time = current_milli_time()

#
# End the timer
#
def end(label):
  log.info('timer', f"'{label}' took {current_milli_time() - start_time}ms")
