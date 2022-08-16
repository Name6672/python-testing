

class BlockGrid:
  def __init__(self,hori_blocks,vert_blocks,default_value=0):
    self.blocks = self.create_blocks_container(hori_blocks,vert_blocks,default_value)
  def create_blocks_container(self,hori:int,vert:int,value=0):
    blocks = {}
    for a in range(vert):
      col = {}
      for b in range(hori):
        col.update({b:value})
      blocks.update({a:col})
    return blocks
  def get_block(self,x,y):
    return self.blocks[y][x]
  def set_block(self,x,y,value):
    self.blocks[y][x] = value
  def number_of_blocks(self):
    vertical = len(self.blocks)
    horizontal = 0
    for col in self.blocks:
      horizontal += len(self.blocks[col])
    return horizontal,vertical
  
  

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