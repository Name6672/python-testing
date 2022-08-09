import pygame
import utilities 
import math

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
  
  def colour_blocks(surf,grid:BlockGrid,blocksize,black_white:bool=False):
    hori_blocks,vert_blocks = grid.number_of_blocks()
    for col in range(vert_blocks):
      for block in range(int(hori_blocks/vert_blocks)):
        draw_area = pygame.Rect((blocksize*block,blocksize*col),(blocksize,blocksize))
        block_colour = (0,0,0)
        if not black_white:
          block_colour = grid.get_block(block,col)
        elif grid.get_block(block,col):
          block_colour = (255,255,255)
        pygame.draw.rect(surf,block_colour,draw_area)
        
  def make_checker_board(grid:BlockGrid):
    hori_blocks,vert_blocks = grid.number_of_blocks()
    for col in range(vert_blocks):
      for block in range(int(hori_blocks/vert_blocks)):
        grid.set_block(block,col,utilities.is_even(col) ^ utilities.is_even(block))
        
    
  
  block_size = 20
  vertical_blocks = int(height/block_size)
  horizontal_blocks = int(width/block_size)
  
  colour_grid = BlockGrid(horizontal_blocks,vertical_blocks,False)
  # colour_grid.set_block(0,0,(255,0,0))
  make_checker_board(colour_grid)
  print(colour_grid.blocks)
  
  def change_pix_to_pos(pix:int):
    pos_x = math.floor(pix[0]/block_size)
    pos_y = math.floor(pix[1]/block_size)
    return (pos_x,pos_y)
  def change_pos_to_pix(pos:int,centred:bool=False):
    pix_x = pos[0]*block_size
    pix_y = pos[1]*block_size
    if centred:
      pix_x+=block_size/2
      pix_y+=block_size/2
    return (pix_x,pix_y)
  
  t = 0
  ticks = 0
  mouse_pos = (0,0)
  mouse_down = False
  
  running = True
  while running:
    screen.fill(background_colour)
    # utilities.text_to_screen(screen,'Hello, World!',(width/2,height/2),background=True)
    dt = clock.get_time()/1000
    t+=dt
    for event in pygame.event.get():
      if event.type == pygame.MOUSEMOTION:
        mouse_pos = pygame.mouse.get_pos()
        if mouse_down:
          pos = change_pix_to_pos(mouse_pos)
          if colour_grid.get_block(pos[0],pos[1]) != set_to:
            colour_grid.set_block(pos[0],pos[1],set_to)
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          pos = change_pix_to_pos(mouse_pos)
          print('mouse pos: ' + str(mouse_pos))
          print('pos: ' + str(pos))
          print('pix: ' + str(change_pos_to_pix(pos)))
          set_to = not colour_grid.get_block(pos[0],pos[1])
          mouse_down = True
          colour_grid.set_block(pos[0],pos[1],set_to)
      elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
          mouse_down = False
          
      elif event.type == pygame.QUIT:
        pygame.quit()
    
    colour_blocks(screen,colour_grid,block_size,True)
          
    pygame.display.flip()
    pygame.display.update()
    ticks += 1
    clock.tick(fps)
  
  print('exiting main')
  
if __name__ == '__main__':
  main()