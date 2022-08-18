



class Neighbour:
  def __init__(self,value,name,pos):
    self.value = value
    self.name = name
    self.pos = pos

class BlockGrid:
  def __init__(self,hori_blocks,vert_blocks,default_value=0):
    self.blocks = self.create_blocks_container(hori_blocks,vert_blocks,default_value)
    self.num_blocks = None
    self.number_of_blocks()
  def create_blocks_container(self,hori:int,vert:int,value=0):
    blocks = {}
    for a in range(vert):
      col = {}
      for b in range(hori):
        col.update({b:value})
      blocks.update({a:col})
    return blocks
  def get_block(self,x,y):
    total_blocks, veti_blocks = self.num_blocks
    hori_blocks = int(total_blocks/veti_blocks)
    if x < hori_blocks and y < veti_blocks and x >= 0 and y >= 0:
      blocks = self.blocks[y][x]
      return blocks
    else:
      return 0x000000
  def set_block(self,x,y,value):
    self.blocks[y][x] = value
  def number_of_blocks(self):
    if self.num_blocks:
      return self.num_blocks
    else:
      vertical = len(self.blocks)
      horizontal = 0
      for col in self.blocks:
        horizontal += len(self.blocks[col])
      self.num_blocks = horizontal, vertical
      return horizontal,vertical
  def get_neighbours(self,x,y):
    total_blocks, vertical_blocks = self.num_blocks
    hori_blocks = total_blocks/vertical_blocks
    north,east,south,west = None,None,None,None
    if y > 1:
      north = Neighbour(self.get_block(x,y-1),'north',(x,y-1))
    if x < hori_blocks-1:
      east = Neighbour(self.get_block(x+1,y),'east',(x+1,y))
    if y < vertical_blocks-1:
      south = Neighbour(self.get_block(x,y+1),'south',(x,y+1))
    if x > 1:
      west = Neighbour(self.get_block(x-1,y),'west',(x-1,y))
    neighbours = [north,east,south,west]
    return neighbours
  
  

def save_grid(grid:BlockGrid):
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