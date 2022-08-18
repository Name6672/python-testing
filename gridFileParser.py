from ast import Try
from optparse import Values
from blockGrid import BlockGrid

def parse_string(string:str):
  if string == 'False':
    return False
  elif string == 'True':
    return True
  else:
    colour = []
    values = string.strip('()')
    values = values.split(',')
    for value in values:
      colour.append(int(value))
    return (colour[0],colour[1],colour[2])
      
    
def make_grid(grid:BlockGrid,rows):
  total_blocks,vert_blocks = grid.number_of_blocks()
  hori_blocks = int(total_blocks/vert_blocks)
  for col in range(hori_blocks):
    for block in range(vert_blocks):
        grid.set_block(col,block,rows[block][col])
    
    
def parse_file(filename:str):
  with open(filename,'r') as file:
    content = file.readlines()
    
    parsed_lines = []
    for line in content:
      collecting = False
      line_strings = []
      current_string = ''
      
      for char in line:
        if char == '<':
          collecting = True
          # current_string += char
          print('added start')
        elif char == '>':
          collecting = False
          # current_string += char
          line_strings.append(current_string)
          current_string = ''
          print('added end')
        elif collecting:
          current_string += char
          print('added char')
      parsed_lines.append(line_strings)

    rows = []
    for line in parsed_lines:
      # print(line)
      objects = []
      for string in line:
        obj = parse_string(string)
        objects.append(obj)
      rows.append(objects)
    # for row in rows:
    #   print(row)
    grid_height = len(rows)
    print(f'height: {grid_height}')
    grid_objects = 0
    for row in rows:
      for obj in row:
        grid_objects += 1
    grid_width = grid_objects/grid_height
    print(f'width: {grid_width}')
    print(f'width * height: {grid_width * grid_height}')
    print(f'total blocks: {grid_objects}')
    print('creating grid')
    grid = BlockGrid(int(grid_width),int(grid_height))
    make_grid(grid,rows)
    print('grid created. returning grid')
    return grid
    
if __name__ == '__main__':
  parse_file('grid_saved_output.txt')