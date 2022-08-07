def print_all(directory):
  for name in directory:
    if not name.startswith('__'):
        value = eval(name)
        print(f'{name}: type = {type(value)}, value = {value}')

