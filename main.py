from modules import epaper, config, log
from modes.hourly import run_hourly
from modes.minutely import run_minutely

config.require(['MODE'])

################################## Main loop ###################################

#
# The main function
#
def main():
  mode = config.get('MODE')

  if mode == 'hourly':
    run_hourly()
  elif mode == 'minutely':
    run_minutely()
  else:
    raise Exception(f'Invalid mode: {mode}')

if __name__ in '__main__':
  try:
    main()
  except KeyboardInterrupt:
    log.error('main', 'Exiting')
    epaper.deinit()
    exit()
