from modules import epaper, config, log
from modes.summary import run_summary
from modes.detailed import run_detailed

config.require(['MODE'])

################################## Main loop ###################################

#
# The main function
#
def main():
  mode = config.get('MODE')

  if mode == 'summary':
    run_summary()
  elif mode == 'detailed':
    run_detailed()
  else:
    raise Exception(f'Invalid mode: {mode}')

if __name__ in '__main__':
  try:
    main()
  except KeyboardInterrupt:
    log.error('main', 'Exiting')
    epaper.deinit()
    exit()
