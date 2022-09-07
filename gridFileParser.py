from blockGrid import BlockGrid

def parse_string(string:str): #turns string into aa value for the grid
  if string == 'False':
    return False
  elif string == 'True':
    return True
  
  else:
    colour = [] # prepare list for the colours
    values = string.strip('()') # remove brackets from the values
    values = values.split(',') # seperate values by commas
    for value in values:
      colour.append(int(value)) # add each value to colour list
    return (colour[0],colour[1],colour[2]) # return as a 3d tuple colour
      
    
def make_grid(grid:BlockGrid,rows): # creates the grid object
  total_blocks,vert_blocks = grid.number_of_blocks()
  hori_blocks = int(total_blocks/vert_blocks)
  for col in range(hori_blocks):
    for block in range(vert_blocks):
        grid.set_block(col,block,rows[block][col])
    
    
def parse_file(filename:str): #parses the file into a grid object
  with open(filename,'r') as file:
    content = file.readlines() # seperate file into lines
    
    parsed_lines = [] # list of all lines after parsing
    for line in content: # read each line
      collecting = False #flag for when inside an object
      line_strings = [] # list of usable strings in the line
      current_string = '' # string being worked with
      
      for char in line: # read each character
        if char == '<': # if the character is a start bracket log that it was found and start collecting
          collecting = True
          print('added start')
          
        elif char == '>': # if character is an end bracket
          collecting = False # stop collecting
          line_strings.append(current_string)# add string to the lines list of parsed strings
          current_string = '' # reset current string
          print('added end') # log end of string
          
        elif collecting:
          current_string += char # add char to string
          print('added char') # log char added
          
      parsed_lines.append(line_strings) # add line to parsed lines

    rows = [] # list of each row
    for line in parsed_lines: # parse each line into a objects
      objects = []
      for string in line:
        obj = parse_string(string)
        objects.append(obj)
      rows.append(objects)
    
    grid_height = len(rows) # set the height of the grid
    print(f'height: {grid_height}') # log the height of the grid
    grid_objects = 0
    for row in rows: # count the amount of objects in the grid
      for obj in row:
        grid_objects += 1
    grid_width = grid_objects/grid_height # set the width of the grid
    print(f'width: {grid_width}') # log width
    print(f'width * height: {grid_width * grid_height}') # log width by height and total blocks for sanity checking
    print(f'total blocks: {grid_objects}')
    print('creating grid') # log that the grid is being created
    grid = BlockGrid(int(grid_width),int(grid_height)) # create the grid
    make_grid(grid,rows)
    print('grid created. returning grid') # log the creation of the grid
    return grid # return the grid
    
if __name__ == '__main__': # test the parser 
  parse_file('grid_saved_output.txt')