class Neighbour: # class for holding info about neighbouring blocks
  def __init__(self,value,name,pos):
    self.value = value
    self.name = name
    self.pos = pos

class BlockGrid: # grid class
  
  def __init__(self,hori_blocks,vert_blocks,default_value=0): # create the grid 
    self.blocks = self.create_blocks_container(hori_blocks,vert_blocks,default_value)
    self.num_blocks = None # pre run the number of blocks function
    self.number_of_blocks()
    
  def create_blocks_container(self,hori:int,vert:int,value=0): # create the dictionaries for the grid
    blocks = {}
    for a in range(vert):
      col = {}
      for b in range(hori):
        col.update({b:value})
      blocks.update({a:col})
    return blocks
  
  def get_block(self,x,y): # get a block in the grid
    total_blocks, veti_blocks = self.num_blocks
    hori_blocks = int(total_blocks/veti_blocks)
    if x < hori_blocks and y < veti_blocks and x >= 0 and y >= 0: # limit value to only those in range
      blocks = self.blocks[y][x]
      return blocks
    else:
      return 0x000000 #return black as default value
    
  def set_block(self,x,y,value): # set a block in the grid
    self.blocks[y][x] = value
    
  def number_of_blocks(self): # return the number of blocks in the grid
    
    if self.num_blocks: # return the value already saved if it exists
      return self.num_blocks
    else: # set the number of blocks if it doesn't
      vertical = len(self.blocks)
      horizontal = 0
      for col in self.blocks:
        horizontal += len(self.blocks[col])
      self.num_blocks = horizontal, vertical
      return horizontal,vertical
    
  def get_neighbours(self,x,y): # get the neighbouring blocks and their information
    total_blocks, vertical_blocks = self.num_blocks
    hori_blocks = total_blocks/vertical_blocks # get the number of blocks in the grid for value limiting
    
    north,east,south,west = None,None,None,None # define the variables for the neighbours
    
    northeast,southwest = None,None
    southeast,northwest = None,None
    
    x_greater = x > 1 # define compare values for limiting
    y_greater = y > 1
    x_less = x < hori_blocks-1
    y_less = y < vertical_blocks-1
    
    if y_greater: # get the primary neighbours
      north = Neighbour(self.get_block(x,y-1),'north',(x,y-1))
    if x_less:
      east = Neighbour(self.get_block(x+1,y),'east',(x+1,y))
    if y_less:
      south = Neighbour(self.get_block(x,y+1),'south',(x,y+1))
    if x_greater:
      west = Neighbour(self.get_block(x-1,y),'west',(x-1,y))
      
    if x_greater and y_greater: # get the secondary neighbours
      northwest = Neighbour(self.get_block(x-1,y-1),'northwest',(x-1,y-1))
    if x_less and y_greater:
      northeast = Neighbour(self.get_block(x+1,y-1),'northeast',(x+1,y-1))
    if x_greater and y_less:
      southwest = Neighbour(self.get_block(x-1,y+1),'southwest',(x-1,y+1))
    if x_less and y_less:
      southeast = Neighbour(self.get_block(x+1,y+1),'southeast',(x+1,y+1))
      
    neighbours = [north,east,south,west,northeast,southwest,southeast,northwest] # pack neighbours into a list
    return neighbours # return all neighbours
  
  

def save_grid(grid:BlockGrid): # save the grid to a text file
  hori_blocks,vert_blocks = grid.number_of_blocks()
  with open('grid_saved_output.txt','w') as file:
    lines = []
    for col in range(vert_blocks):
      line = ''
      for block in range(int(hori_blocks/vert_blocks)):
        line += (' <' + str(grid.get_block(block,col)) + '> ')
      lines.append((line + '\n'))
      print('saving line...')
    file.writelines(lines)
    file.close()
    print('saved file')
    
if __name__ == '__main__':
  grid = BlockGrid(10,10)
  print(grid.number_of_blocks())