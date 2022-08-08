import pygame
import utilities 

#globals
screen_size = width, height = (600,400)
fps = 60
background_colour = 0x000000
pygame.init()
screen = pygame.display.set_mode(screen_size)

clock = pygame.time.Clock()

class BlockGrid:
  def __init__(self,hori_blocks,vert_blocks,default_value=0):
    self.blocks = self.create_blocks_container(hori_blocks,vert_blocks,default_value)
  def create_blocks_container(self,hori,vert,value=0):
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


def main():
  
  def colour_blocks(surf,grid:BlockGrid,blocksize):
    hori_blocks,vert_blocks = grid.number_of_blocks()
    for col in range(vert_blocks):
      for block in range(int(hori_blocks/vert_blocks)):
        draw_area = pygame.Rect((blocksize*block,blocksize*col),(blocksize,blocksize))
        block_colour = grid.get_block(block,col)
        pygame.draw.rect(surf,block_colour,draw_area)
    
  
  block_size = 20
  vertical_blocks = int(height/block_size)
  horizontal_blocks = int(width/block_size)
  
  colour_grid = BlockGrid(horizontal_blocks,vertical_blocks,(0,255,0))
  colour_grid.set_block(0,0,(255,0,0))
  print(colour_grid.blocks)
  
  
  t = 0
  ticks = 0
  mouse_pos = (0,0)
  
  running = True
  while running:
    # screen.fill(background_colour)
    # utilities.text_to_screen(screen,'Hello, World!',(width/2,height/2),background=True)
    dt = clock.get_time()/1000
    t+=dt
    for event in pygame.event.get():
      if event.type == pygame.MOUSEMOTION:
        mouse_pos = pygame.mouse.get_pos()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          print('clicky')
    
    colour_blocks(screen,colour_grid,block_size)
          
    pygame.display.flip()
    pygame.display.update()
    ticks += 1
    clock.tick(fps)
  
  print('exiting main')
  
if __name__ == '__main__':
  main()