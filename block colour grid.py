import sys
import pygame
import utilities 
import math
from blockGrid import BlockGrid
from blockGrid import save_grid
from blockGrid import Neighbour
import gridFileParser

#globals
screen_size = width, height = (600,400)
fps = 10000#LIESSSS
background_colour = 0x000000
pygame.init()
screen = pygame.display.set_mode(screen_size)
GRID_SAVE_FILE = 'grid_saved_output.txt'

clock = pygame.time.Clock()



def main():
  
  def load_grid(filename:str):
    grid = gridFileParser.parse_file(filename)
    return grid
  
  checker_colour_dict = {
    True:(175,100,100),
    False:(0,150,0)
  }
  
  def dist(pos_1,pos_2):
    x1,y1 = pos_1
    x2,y2 = pos_2
    x = x2 - x1
    y = y2 - y1
    return x,y
  
  def colour_blocks(surf,grid:BlockGrid):
    hori_blocks,vert_blocks = grid.number_of_blocks()
    for col in range(vert_blocks):
      for block in range(int(hori_blocks/vert_blocks)):
        draw_area = pygame.Rect((block,col),(1,1))
        block_colour = (0,0,0)
        block_value = grid.get_block(block,col)
        if type(block_value) == type(True):
          block_colour = checker_colour_dict[block_value]
        else:
          block_colour = block_value
        pygame.draw.rect(surf,block_colour,draw_area)
    # hori_blocks,vert_blocks = grid.number_of_blocks() #OLD VERSION
    # cam_x,cam_y = change_pos_to_pix(cam_pos)
    # for col in range(vert_blocks):
    #   for block in range(int(hori_blocks/vert_blocks)):
    #     x_dist,y_dist = dist((block - camera_width/2,col - camera_height/2),cam_pos)
    #     if abs(x_dist) < (camera_width/2 + 1) and abs(y_dist) < (camera_height/2 + 1):
    #       draw_area = pygame.Rect(((blocksize*block) - cam_x,(blocksize*col)- cam_y),(blocksize,blocksize))
    #       block_colour = (0,0,0)
    #       block_value = grid.get_block(block,col)
    #       if type(block_value) == type(True):
    #         block_colour = checker_colour_dict[block_value]
    #       else:
    #         block_colour = block_value
    #       pygame.draw.rect(surf,block_colour,draw_area)

        
  def make_checker_board(grid:BlockGrid): #deprecated
    total_blocks,vert_blocks = grid.number_of_blocks()
    hori_blocks = int(total_blocks/vert_blocks)
    for col in range(vert_blocks):
      for block in range(hori_blocks):
        if utilities.is_border(block,col,hori_blocks,vert_blocks):
          grid.set_block(block,col,(0,0,255))
        else:
          grid.set_block(block,col,utilities.is_even(col) ^ utilities.is_even(block))
          
  def is_next_to_true(grid,col,block):
    a = grid.get_block(block-1,col)
    b = grid.get_block(block+1,col)
    c = grid.get_block(block,col-1)
    d = grid.get_block(block,col+1)
    return (a or b or c or d)
          
  def make_game_board(grid:BlockGrid):
    total_blocks,vert_blocks = grid.number_of_blocks()
    hori_blocks = int(total_blocks/vert_blocks)
    for col in range(vert_blocks):
      for block in range(hori_blocks):
        if utilities.is_border(block,col,hori_blocks,vert_blocks):
          grid.set_block(block,col,(0,0,0))
        else:
          grid.set_block(block,col,False)
          def two_true_false():
            return utilities.random_true_or_false() and utilities.random_true_or_false()
          win_random = two_true_false() and two_true_false and utilities.random_true_or_false()
          if win_random or (two_true_false() and is_next_to_true(grid,col,block)):
            grid.set_block(block,col,True)
  
  factors_w = utilities.factors(width)
  factors_h = utilities.factors(height)
  factors_common = utilities.in_both(factors_w,factors_h)
  
  print(f'factors of {width}: {factors_w}')
  print(f'factors of {height}: {factors_h}')
  print(f'common factors: {factors_common}')
  
  block_index = 6
  block_size = factors_common[block_index]
  print(block_size)
  def update_block_size():
    nonlocal block_size
    block_size = factors_common[block_index]
  horizontal_blocks = int(60)
  vertical_blocks = int(40)
  
  camera_size = camera_width,camera_height = (width/block_size,height/block_size)
  
  def update_camera_size():
    nonlocal camera_size
    nonlocal camera_width
    nonlocal camera_height
    camera_size = camera_width,camera_height = (width/block_size,height/block_size)
  
  colour_grid = BlockGrid(horizontal_blocks,vertical_blocks,False)
  # colour_grid.set_block(0,0,(255,0,0))
  make_game_board(colour_grid)
  # print(colour_grid.blocks)
  
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
  last_move = -1000
  mouse_pos = (0,0)
  mouse_down = False
  total_blocks,vert_blocks = colour_grid.number_of_blocks()
  hori_blocks = int(total_blocks/vert_blocks)
  
  outlines = True
  
  # blocks_image = pygame.Surface((600,600))
  # colour_blocks(blocks_image,colour_grid)
  def draw_camera(surf,cam_pos,blocksize,grid):
    cam_x, cam_y = cam_pos
    for col in range(int(camera_height)):
      for block in range(int(camera_width)):
        draw_area = pygame.Rect(((blocksize*block),(blocksize*col)),(blocksize,blocksize))
        block_colour = (0,0,0)
        cam_offset = (cam_x, cam_y)
        block_value = 0x000000
        block_value = grid.get_block(block + cam_offset[0] ,col+ cam_offset[1])
        if type(block_value) == type(True):
          block_colour = checker_colour_dict[block_value]
        else:
          block_colour = block_value
        pygame.draw.rect(surf,block_colour,draw_area)
        if outlines:
          neighbours = grid.get_neighbours(block + cam_offset[0] ,col+ cam_offset[1])
          for neighbour in neighbours:
            if neighbour.name == 'north' and not block_value == neighbour.value:
              pygame.draw.line(surf,0x000000,draw_area.topleft,draw_area.topright)
            if neighbour.name == 'east' and not block_value == neighbour.value:
              pygame.draw.line(surf,0x000000,draw_area.topright,draw_area.bottomright)
            if neighbour.name == 'south' and not block_value == neighbour.value:
              pygame.draw.line(surf,0x000000,draw_area.bottomleft,draw_area.bottomright)
            if neighbour.name == 'west' and not block_value == neighbour.value:
              pygame.draw.line(surf,0x000000,draw_area.topleft,draw_area.bottomleft)
  
  
  camera_pos = (hori_blocks/2,vert_blocks/2)
  
  running = True
  while running:
    screen.fill(background_colour)
    # utilities.text_to_screen(screen,'Hello, World!',(width/2,height/2),background=True)
    dt = clock.get_time()/1000
    # print(dt)
    t+=dt
    cam_x, cam_y = camera_pos
    
    for event in pygame.event.get():
      if event.type == pygame.MOUSEMOTION:
        mouse_pos = pygame.mouse.get_pos()
        if mouse_down:
          pos = change_pix_to_pos(mouse_pos)
          pos = (pos[0] + cam_x, pos[1] + cam_y)
          if colour_grid.get_block(pos[0],pos[1]) != set_to and not utilities.is_border(pos[0],pos[1],hori_blocks,vert_blocks):
            colour_grid.set_block(pos[0],pos[1],set_to)
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          pos = change_pix_to_pos(mouse_pos)
          pos = (pos[0] + cam_x, pos[1] + cam_y)
          block_val = colour_grid.get_block(pos[0],pos[1])
          border = utilities.is_border(pos[0],pos[1],hori_blocks,vert_blocks)
          # print('\n')
          # print('mouse pos: ' + str(mouse_pos))
          # print('pos: ' + str(pos))
          # print('pix: ' + str(change_pos_to_pix(pos)))
          # print(f'border: {border}')
          # if type(block_val) == type(True):
          #   print(f'value: {checker_colour_dict[block_val]}')
          # else:
          #   print(f'value: {block_val}')
          set_to = not block_val
          mouse_down = True
          if not border:
            colour_grid.set_block(pos[0],pos[1],set_to)
        elif event.button == 3:#right click
          pos = change_pix_to_pos(mouse_pos)
          pos = (pos[0] + cam_x, pos[1] + cam_y)
          block_val = colour_grid.get_block(pos[0],pos[1])
          border = utilities.is_border(pos[0],pos[1],hori_blocks,vert_blocks)
          print('\n')
          print('mouse pos: ' + str(mouse_pos))
          print('pos: ' + str(pos))
          print('pix: ' + str(change_pos_to_pix(pos)))
          print(f'border: {border}')
          if type(block_val) == type(True):
            print(f'value: {checker_colour_dict[block_val]}')
          else:
            print(f'value: {block_val}')
        elif event.button == 4:#scroll up
          block_index += 1
          if block_index > len(factors_common) - 1:
            block_index = len(factors_common) - 1
          update_block_size()
          update_camera_size()
        elif event.button == 5:#scroll down
          block_index -= 1
          if block_index < 0:
            block_index = 0
          update_block_size()
          update_camera_size()
          if camera_width > hori_blocks:
            block_index += 1
            update_block_size()
            update_camera_size()
          if camera_height > vert_blocks:
            block_index += 1
            update_block_size()
            update_camera_size()
      elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
          mouse_down = False
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_F5:
          save_grid(colour_grid)
        elif event.key == pygame.K_F6:
          colour_grid = load_grid(GRID_SAVE_FILE)
          total_blocks,vert_blocks = colour_grid.number_of_blocks()
          hori_blocks = int(total_blocks/vert_blocks)
        elif event.key == pygame.K_o:
          outlines = not outlines
          
      elif event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
        
    keys = pygame.key.get_pressed()
    new_cam_x, new_cam_y = camera_pos
    if keys[pygame.K_w]:
      new_cam_y -= 1
    if keys[pygame.K_s]:
      new_cam_y += 1

    if keys[pygame.K_a]:
      new_cam_x -= 1
    if keys[pygame.K_d]:
      new_cam_x += 1
      
    if new_cam_y < 0:
      new_cam_y = 0
    elif new_cam_y > vert_blocks - (camera_height):
      new_cam_y = vert_blocks - (camera_height)

    if new_cam_x < 0:
      new_cam_x = 0
    elif new_cam_x > hori_blocks - (camera_width):
      new_cam_x = hori_blocks - (camera_width)
    
    new_camera_pos = (new_cam_x,new_cam_y)
    if t - last_move > 0.1:
      camera_pos = new_camera_pos
      last_move = t
      mouse_pos = pygame.mouse.get_pos()
    # print(t)
    
    
    draw_camera(screen,camera_pos,block_size,colour_grid)
    true_fps = clock.get_fps()
    utilities.text_to_screen(screen,str(round(true_fps,1)),(0,0),15)
          
    pygame.display.flip()
    pygame.display.update()
    ticks += 1
    clock.tick(fps)
  
  print('exiting main')
  
if __name__ == '__main__':
  main()