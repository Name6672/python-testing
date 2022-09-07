import sys # for sys.exit that's about it
import pygame # visual engine
import utilities # my various functions
import math #for MATHS
from blockGrid import BlockGrid # block grid class created for this program
from blockGrid import save_grid #f function to save a grid to pre-specified file
import gridFileParser # parser for loading grid files


#BUG TRACKER
#ALL BUGS FIXED :D
#tho sometimes (when you zoom out too much) it's slow

#globals
screen_size = width, height = (1200,800) # size of the screen in pixels
fps = 10000#LIESSSS #set target fps for pygame
background_colour = 0x000000 #black
pygame.init() # initialise pygame
screen = pygame.display.set_mode(screen_size) # initialise the screen
#constants
GRID_SAVE_FILE = 'grid_saved_output.txt'
STARTING_GRID_SIZE = SGW, SGH = (240,240)

#create the clock
clock = pygame.time.Clock()

#setup sounds
# place_sound_a = pygame.mixer.Sound('place_sound_a.wav')
# place_sound_b = pygame.mixer.Sound('place_sound_b.wav')
# place_sound_c = pygame.mixer.Sound('place_sound_c.wav')
# place_sounds = [place_sound_a,place_sound_b,place_sound_c]


def make_checker_board(grid:BlockGrid,border = False): #deprecated checker board function
  total_blocks,vert_blocks = grid.number_of_blocks()
  hori_blocks = int(total_blocks/vert_blocks)
  for col in range(vert_blocks):
    for block in range(hori_blocks):
      if utilities.is_border(block,col,hori_blocks,vert_blocks) and border:
        grid.set_block(block,col,(0,0,255))
      else:
        grid.set_block(block,col,utilities.is_even(col) ^ utilities.is_even(block))


def dist(pos_1,pos_2):#get the distance between two points as x and y values
  x1,y1 = pos_1
  x2,y2 = pos_2
  x = x2 - x1
  y = y2 - y1
  return x,y


def main(): #main function
  
  colours = [
    (15,15,15),
    (255,255,255),
    (255,0,0),
    (0,255,0),
    (0,0,255),
    (175,100,100),
    (0,150,0)
  ]
  
  def load_grid(filename:str):# calls file parser function to load file
    grid = gridFileParser.parse_file(filename)
    return grid
  
  checker_colour_dict = { # dictionary to convert from true false to colours
    True:(175,100,100),
    False:(0,150,0)
  }
  
  def colour_blocks(surf,grid:BlockGrid):#deprecated function for drawing blocks to a surface (the screen)
    hori_blocks,vert_blocks = grid.number_of_blocks()
    for col in range(vert_blocks): # for each collum but actually probably rows i have no idea how my own grid code works it's really bad actually-
      for block in range(int(hori_blocks/vert_blocks)): # for each block in a collum
        draw_area = pygame.Rect((block,col),(1,1)) # rectangle (square) it will draw
        block_colour = (0,0,0) # define block colour
        block_value = grid.get_block(block,col)
        if type(block_value) == type(True):
          block_colour = checker_colour_dict[block_value]
        else:
          block_colour = block_value
        pygame.draw.rect(surf,block_colour,draw_area)
          
  def is_next_to_true(grid,col,block): # returns true if any of the neighbouring blocks aren't a 0 value
    a = grid.get_block(block-1,col)
    b = grid.get_block(block+1,col)
    c = grid.get_block(block,col-1)
    d = grid.get_block(block,col+1)
    return (a or b or c or d)
          
  def make_game_board(grid:BlockGrid): # makes the starting board for the "game"
    total_blocks,vert_blocks = grid.number_of_blocks()
    hori_blocks = int(total_blocks/vert_blocks)
    for col in range(vert_blocks):
      for block in range(hori_blocks):
        if utilities.is_border(block,col,hori_blocks,vert_blocks):
          grid.set_block(block,col,(0,0,0),True)
        else:
          grid.set_block(block,col,False,True)
          def two_true_false(): # function for checking random twice to reduce odds from 50% to 25%
            return utilities.random_true_or_false() and utilities.random_true_or_false()
          win_random = two_true_false() and two_true_false and utilities.random_true_or_false() # one in 32 chance
          if win_random or (two_true_false() and is_next_to_true(grid,col,block)): # makes it more likely if the block is next to a true value to make "veins" more likely
            grid.set_block(block,col,True,True)
  
  factors_w = utilities.factors(width)
  factors_h = utilities.factors(height)
  factors_common = utilities.in_both(factors_w,factors_h) # gets the common factors of width and height, which will be used to determine safe blocksizes to use for the camera zoom
  
  horitzontal_minimum = width/SGW
  vertical_minimum = height/SGH
  block_size_minimum = max(vertical_minimum,horitzontal_minimum)
  print(f'vert_min: {vertical_minimum}\nhori_min: {horitzontal_minimum}\nmin_size: {block_size_minimum}\n')
  block_size_list = utilities.limit_values(factors_common,block_size_minimum)
  
  print(f'factors of {width}: {factors_w}')
  print(f'factors of {height}: {factors_h}')
  print(f'common factors: {factors_common}')
  print(f'size list: {block_size_list}')
  
  block_index = int(len(block_size_list)/2)
  block_size = block_size_list[block_index]
  print(block_size)
  
  def update_block_size():# updates block size so that only index needs changing
    nonlocal block_size
    block_size = block_size_list[block_index]
  
  horizontal_blocks = int(SGW)# number of blocks in grid, defined by a global constant
  vertical_blocks = int(SGH)
  
  camera_size = camera_width,camera_height = (width/block_size,height/block_size)# size of the camera in grid spaces
  
  def update_camera_size():# updates the camera size
    nonlocal camera_size
    nonlocal camera_width
    nonlocal camera_height
    camera_size = camera_width,camera_height = (width/block_size,height/block_size)
  
  colour_grid = BlockGrid(horizontal_blocks,vertical_blocks,False)# create the grid for the "game"
  
  make_game_board(colour_grid)# update the grid to a "game" board
  
  
  def change_pix_to_pos(pix:int):# changes from a position in pixels to a position on the grid
    pos_x = math.floor(pix[0]/block_size)
    pos_y = math.floor(pix[1]/block_size)
    return (pos_x,pos_y)
  def change_pos_to_pix(pos:int,centred:bool=False): #changes from a position on the grid to a position in pixels
    pix_x = pos[0]*block_size
    pix_y = pos[1]*block_size
    if centred:
      pix_x+=block_size/2
      pix_y+=block_size/2
    return (pix_x,pix_y)
  
  t = 0# time
  ticks = 0 # frames
  last_move = -1000 # last time camera moved
  mouse_pos = (0,0) # position of the mouse
  mouse_down = False # if the left mouse button is held down
  #number of blocks in the grid
  total_blocks,vert_blocks = colour_grid.number_of_blocks() 
  hori_blocks = int(total_blocks/vert_blocks)
  
  outlines = True# whether block differences should have a black outline
  
  
  camera_buffer = pygame.Surface((width,height)) # saves the camera view so that it doesn't have to be calcuated unless necessary
  
  def draw_camera(surf,cam_pos,blocksize,grid,pos=None,direct_value=None,is_first:bool=True): # updates camera view
    cam_x, cam_y = cam_pos
    cam_offset = (cam_x, cam_y) #literally the exact same as cam_pos idk why i made this
    
    if pos: #only calculate a defined position to reduce total caluations and increase frame rate
      draw_area = pygame.Rect(((blocksize*(pos[0] - cam_offset[0])),(blocksize*(pos[1] - cam_offset[1]))),(blocksize,blocksize))
      block_colour = (0,0,0)
      block_value = direct_value
      if block_value != None:
        if type(block_value) == type(True):
          block_colour = checker_colour_dict[block_value]
        else:
          block_colour = block_value
        pygame.draw.rect(surf,block_colour,draw_area)
      else:
        block_value = grid.get_block(pos[0], pos[1])
        if type(block_value) == type(True):
          block_colour = checker_colour_dict[block_value]
        else:
          block_colour = block_value
      if outlines: # draw the outlines where diferent colours meet
        neighbours = grid.get_neighbours(pos[0],pos[1])
        for neighbour in neighbours:
          if neighbour != None:
            neighbour_pos = (neighbour.pos[0],neighbour.pos[1])
            if neighbour.name == 'north' and not block_value == neighbour.value:
              pygame.draw.line(surf,0x000000,draw_area.topleft,draw_area.topright)
            elif neighbour.name == 'east' and not block_value == neighbour.value:
              pygame.draw.line(surf,0x000000,draw_area.topright,draw_area.bottomright)
            elif neighbour.name == 'south' and not block_value == neighbour.value:
              pygame.draw.line(surf,0x000000,draw_area.bottomleft,draw_area.bottomright)
            elif neighbour.name == 'west' and not block_value == neighbour.value:
              pygame.draw.line(surf,0x000000,draw_area.topleft,draw_area.bottomleft)
            if is_first:
              draw_camera(surf,cam_pos,blocksize,grid,neighbour_pos,neighbour.value,False) #calculate neighbouring blocks and their outlines
              
    else: # draw entire camera view
      for col in range(int(camera_height)):
        for block in range(int(camera_width)): # for every block visible to camera
          draw_area = pygame.Rect(((blocksize*block),(blocksize*col)),(blocksize,blocksize))
          block_colour = (0,0,0)
          block_value = 0x000000
          block_value = grid.get_block(block + cam_offset[0] ,col+ cam_offset[1])
          if type(block_value) == type(True):
            block_colour = checker_colour_dict[block_value]
          else:
            block_colour = block_value
          pygame.draw.rect(surf,block_colour,draw_area)
          if outlines: # draw the outlines where diferent colours meet
            neighbours = grid.get_neighbours(block + cam_offset[0] ,col+ cam_offset[1])
            for neighbour in neighbours:
              if neighbour != None:
                if neighbour.name == 'north' and not block_value == neighbour.value:
                  pygame.draw.line(surf,0x000000,draw_area.topleft,draw_area.topright)
                elif neighbour.name == 'east' and not block_value == neighbour.value:
                  pygame.draw.line(surf,0x000000,draw_area.topright,draw_area.bottomright)
                elif neighbour.name == 'south' and not block_value == neighbour.value:
                  pygame.draw.line(surf,0x000000,draw_area.bottomleft,draw_area.bottomright)
                elif neighbour.name == 'west' and not block_value == neighbour.value:
                  pygame.draw.line(surf,0x000000,draw_area.topleft,draw_area.bottomleft)
  
  
  camera_pos = (hori_blocks/2,vert_blocks/2) # set top left of camera to the middle
  
  running = True
  set_to = False
  
  while running:
    screen.fill(background_colour)# draw background to ensure nothing is left from previous frame
    
    dt = clock.get_time()/1000# get the change in time from last frame
    
    t+=dt #update time counter
    cam_x, cam_y = camera_pos # get x and y values of the camera position for convenience variables
    camera_changed = False # set to true to update entire camera view
    
    def change_block(pos):
      colour_grid.set_block(pos[0],pos[1],set_to)
      # place_sound = utilities.random_from_list(place_sounds)
      # place_sound.play()
      draw_camera(camera_buffer,camera_pos,block_size,colour_grid,pos,set_to)#redraw specific block
    
    for event in pygame.event.get(): # handle pygame events
      if event.type == pygame.MOUSEMOTION: # when the mouse is moved
        mouse_pos = pygame.mouse.get_pos() #update the mouse position
        if mouse_down: # if the left mouse
          pos = change_pix_to_pos(mouse_pos)
          pos = (pos[0] + cam_x, pos[1] + cam_y) # get the grid position of the mouse
          border = utilities.is_border(pos[0],pos[1],hori_blocks,vert_blocks) # get whether the block is the border of the grid
          if colour_grid.get_block(pos[0],pos[1]) != set_to and not border:
            colour_grid.set_block(pos[0],pos[1],set_to) # drag set blocks
            # place_sound = utilities.random_from_list(place_sounds)
            # place_sound.play()
            draw_camera(camera_buffer,camera_pos,block_size,colour_grid,pos,set_to)#redraw specific block
            
      elif event.type == pygame.MOUSEBUTTONDOWN: 
        # print (f'mouse button {event.button} pressed down')
        if event.button == 1:#left click
          pos = change_pix_to_pos(mouse_pos)
          pos = (pos[0] + cam_x, pos[1] + cam_y) # get the grid position of the mouse
          block_val = colour_grid.get_block(pos[0],pos[1]) # get the value of the block at the mouse position
          border = utilities.is_border(pos[0],pos[1],hori_blocks,vert_blocks) # get whether the block is the border of the grid
          
          set_to = not block_val # the value to set the block to right now and while dragging
          mouse_down = True# say the left mouse is being held down
          if not border: # change the block value if it's not a border block
            change_block(pos)
        elif event.button == 2:#middle click
          pass
            
        elif event.button == 3:#right click
          pos = change_pix_to_pos(mouse_pos)
          pos = (pos[0] + cam_x, pos[1] + cam_y) # get the grid position of the mouse
          block_val = colour_grid.get_block(pos[0],pos[1]) # get the value of the block at the mouse position
          border = utilities.is_border(pos[0],pos[1],hori_blocks,vert_blocks) # get whether the block is the border of the grid
          #print to console information about the block at the mouse position
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
          block_index += 1 # zoom in by increasing amount of pixels on the screen each block takes up
          if block_index > len(factors_common) - 1:
            block_index = len(factors_common) - 1 # prevent out of range errors
          update_block_size()# update block and camera size
          update_camera_size()
          camera_changed = True # redraw camera view
          
        elif event.button == 5:#scroll down
          block_index -= 1 # zoom out by decreasing amount of pixels on the screen each block takes up
          if block_index < 0:# prevent out of range errors
            block_index = 0
          update_block_size()# update block and camera size
          update_camera_size()
          if camera_width > hori_blocks: # prevent the camera zooming out too far
            block_index += 1
            update_block_size()
            update_camera_size()
          if camera_height > vert_blocks:
            block_index += 1
            update_block_size()
            update_camera_size()
          camera_changed = True # redraw camera view
          
        elif event.button == 6: #back extra mouse button
          pass
        
        elif event.button == 7: #forward extra mouse button
          pass
        
      elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:# left click release
          mouse_down = False
          
      elif event.type == pygame.KEYDOWN: # key pressed down
        if event.key == pygame.K_F5:
          save_grid(colour_grid) # save current grid to file
          
        elif event.key == pygame.K_F6:
          colour_grid = load_grid(GRID_SAVE_FILE) # load grid from file
          total_blocks,vert_blocks = colour_grid.number_of_blocks()
          hori_blocks = int(total_blocks/vert_blocks)
          camera_changed = True# redraw camera view
          
        elif event.key == pygame.K_o:
          outlines = not outlines # toggle outlines at borders between diferent colours
          camera_changed = True# redraw camera view 
          
      elif event.type == pygame.QUIT:# close the program when x button clicked
        pygame.quit()
        sys.exit()
        
    keys = pygame.key.get_pressed() # get pressed keys
    new_cam_x, new_cam_y = camera_pos # new camera position for moving 
    is_moving = False # tell when the camera is moving to redraw camera
    
    if keys[pygame.K_w]: # move camera up when w pressed
      new_cam_y -= 1
      is_moving = True
    if keys[pygame.K_s]: # move camera down when s pressed
      new_cam_y += 1
      is_moving = True

    if keys[pygame.K_a]: # move camera left when a pressed
      new_cam_x -= 1
      is_moving = True
    if keys[pygame.K_d]: # move camera right when d pressed
      new_cam_x += 1
      is_moving = True
      
    if new_cam_y < 0: # ensure camera stays inside grid horizontally
      new_cam_y = 0
      is_moving = True
    elif new_cam_y > vert_blocks - (camera_height):
      new_cam_y = vert_blocks - (camera_height)
      is_moving = True

    if new_cam_x < 0: # ensure camera stays inside grid vertically
      new_cam_x = 0
      is_moving = True
    elif new_cam_x > hori_blocks - (camera_width):
      new_cam_x = hori_blocks - (camera_width)
      is_moving = True
    
    new_camera_pos = (new_cam_x,new_cam_y)
    if t - last_move > 0.1 and is_moving: # ensure the camera doesn't move too fast and only call functions if it actually moved
      camera_pos = new_camera_pos # move the camera
      last_move = t 
      camera_changed = True # redraw the camera view
      
    mouse_pos = pygame.mouse.get_pos() # update mouse position
    if mouse_down and is_moving:# if mouse is held down while moving
      pos = change_pix_to_pos(mouse_pos)# get position of the mouse on the grid
      pos = (pos[0] + cam_x, pos[1] + cam_y)
      if colour_grid.get_block(pos[0],pos[1]) != set_to and not utilities.is_border(pos[0],pos[1],hori_blocks,vert_blocks):
        change_block(pos)
    
    
    if camera_changed or ticks == 0: # draw the camera when the view changed and at start
      draw_camera(camera_buffer,camera_pos,block_size,colour_grid)
    screen.blit(camera_buffer,(0,0)) # draw camera to screen
    
    true_fps = clock.get_fps() # get the fps
    utilities.text_to_screen(screen,str(round(true_fps,1)),(0,0),15) # print fps to screen in top left corner
          
    pygame.display.flip() # update display
    pygame.display.update()
    ticks += 1# update tick counter
    clock.tick(fps) # tick the clock
  
  print('exiting main')
  
if __name__ == '__main__': # ensure application only runs when being run as the main application
  main()