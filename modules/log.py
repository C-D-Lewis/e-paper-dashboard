from termcolor import colored

#
# Log info level
#
def info(module_name, content):
  print(colored(f'[{module_name}] {content}', 'dark_grey'))

#
# Log error level
#
def error(module_name, content):
  print(colored(f'[{module_name}] {content}', 'red'))
