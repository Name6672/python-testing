import pygame
import sys
import random
import math
import bisect
import timeit



def get_words(string):
  words = []
  word = ''
  for char in string:
    word += char
    if char == ' ':
      words.append(word)
      word = ''
  words.append(word)
  return words

def convert_s_to_f(string):
  new_string = ''
  for word in get_words(string):
    new_word = ''
    end_index = len(word)-1
    i = 0
    for char in word:
      i+=1
      if char == 's' and i != end_index:
        new_word += 'f'
      else:
        new_word += char
    new_string += new_word
  return new_string

test_string = 'test string hasss tests '
print(convert_s_to_f(test_string))

def get_border(rect,width:int = 1):
  border = pygame.Rect(rect.left,rect.top,rect.width,rect.height)
  border.top -= width
  border.left -= width
  border.width += width*2
  border.height += width*2
  return border

def text_to_img(text, size = 45, color = (255,255,255), back_colour = (0,0,0) ):
  text = str(text)
  font = pygame.font.SysFont('blockhead',  size)
  text = font.render(text,True,color)
  temp_surf = text
  text.fill(back_colour)
  text.blit(temp_surf,(0,0))
  
  return text

def choose_random(list:list):
  i = random.randint(0,len(list)-1)
  return list[i]
def deg(radians):
  return -(radians / math.pi) * 180
def rad(degrees):
  return -(degrees / 180) * math.pi

g = 10

def weighted_random(list):
  """
  Take the weighted random of a list of tuples. tuple[0] will be the value taken, and tuple[1] will be the weight
  """
  l = []
  for tuple in list:
    value,weight = tuple
    for i in range(weight):
      l.append(value)
  return choose_random(l)

def test_weighted(self):

  dif = 4
  mid = 9

  test_list = [
    (0,0),
    (1,0),
    (2,0),
    (3,0),
    (4,0),
    (5,0),
    (6,0),
    (7,0),
    (8,0),
    (9,0),
    (10,0),
    (11,0),
    (12,0),
    (13,0),
    ]
  
  a = 0
  for i in range(len(test_list)):
    a+= 1
    test_list[i] = (i,int(a**(dif/2)))
    if i == mid:
      break
  for i in range(len(test_list)):
    if i > mid:
      a -= 1
      test_list[i] = (i,int(a**(dif/2)))

  

  results = {
    0:0,
    1:0,
    2:0,
    3:0,
    4:0,
    5:0,
    6:0,
    7:0,
    8:0,
    9:0,
    10:0,
    11:0,
    12:0,
    13:0,
    }
  def count(dict):
    i = 0
    for item in dict:
      i+=1
    return i
  len_of = count(results)

  for i in range(1000):
    result = weighted_random(test_list)
    num = results[result]
    results[result] = num + 1


  rects = []
  for result in results:
    percent = (results[result]/10)
    top = height - ((percent /100) * height)
    left = (result/len_of)*width
    right = ((result+1)/len_of)*width
    rect_width = right-left
    bot = height
    rect_height = bot-top
    rect = pygame.Rect(left,top,rect_width,rect_height)
    rects.append(rect)

  pygame.display.set_caption('weighted random graph')
  button_img = pygame.image.load('exit_button.png')
  button_2_img = pygame.image.load('try_again_button.png')

  running = True
  t = 0

  def button_on_click(self):
    nonlocal running
    running = False
  
  def try_again(self):
    nonlocal running
    running = False
    test_weighted(self)

  buttons = []
  exit_button = Button(button_img,'exit button',(20,20),button_on_click)
  try_button = Button(button_2_img,'try button',(20,52),try_again)

  buttons.append(exit_button)
  buttons.append(try_button)
  mouse_pos = (0,0)

  while running:
    screen.fill(background_colour)
    dt = clock.get_time()/1000
    t+=dt
    for event in pygame.event.get():
      if event.type == pygame.MOUSEMOTION:
        mouse_pos = pygame.mouse.get_pos()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          for button in buttons:
            if button.is_in(event.pos):
              button.update(mouse_pos,clicked=True)

    for button in buttons:
      button.update(mouse_pos)
    for rect in rects:
      border = get_border(rect)
      pygame.draw.rect(screen,0xffffff,border)
      pygame.draw.rect(screen,0x0000ff,rect)
      index = rects.index(rect)
      result = index

      text_to_screen(str(result+1),(rect.left,height-10),20)
      text_to_screen(f'{results[result]/10}%',(rect.left,rect.top - 20),20)



    clock.tick()
    pygame.display.flip()
    pygame.display.update()
  pygame.display.set_caption('Menu')

rainbow = [
  0xff0000,
  0xff8000,
  0xffff00,
  0x00ff00,
  0x0000ff,
  0xb000b0,
]

rainbow_rgb = [
  (255,0,0),
  (255,128,0),
  (255,255,0),
  (0,255,0),
  (0,0,255),
  (176,0,176)
]
##Physics
#vavg = d/t
#a = v/t
#v = 2vavg if starting from 0, otherwise take the start and end and use the differnce
#d = 1/2at^2
#e = 1/2mv^2
#fd = 1/2mv^2
#mgd = 1/2mv^2
#gd = 1/2v^2
#d = (1/2v^2)/g
#d = v^2/2g
class Particle:
  def __init__(self,position:tuple, velocity:tuple,colour,life_time = 0,mass = 0.001,glow = False):
    self.pos = position
    self.vel = velocity
    self.colour = colour
    if life_time > 1:
      self.life_time = life_time + round(random.uniform(-0.8,0.8),2)
    else:
      self.life_time = life_time + round(random.uniform(0,1.6),2)
    self.life_length = 0
    self.life_left = self.life_time
    self.mass = mass
    self.forces = []
    self.glow = glow
    self.images = None
  def draw(self):
    if self.images == None:
      #create full alpha circle
      normal = pygame.Surface((5,5))
      normal.set_colorkey((0,0,0))
      normal.fill((0,0,0))

      #create low alpha circle
      low = pygame.Surface((5,5))
      low.set_colorkey((0,0,0))
      low.set_alpha(80)
      low.fill((0,0,0))

      #create lower alpha circle
      lower = pygame.Surface((5,5))
      lower.set_colorkey((0,0,0))
      lower.set_alpha(40)
      lower.fill((0,0,0))

      #draw to images
      pygame.draw.circle(normal,self.colour,(2,2),1,1)
      pygame.draw.circle(low,self.colour,(2,2),3,2)
      pygame.draw.circle(lower,self.colour,(2,2),5,2)
      self.images = [normal,low,lower]
    else:
      normal,low,lower = self.images

    #draw to screen
    if self.life_left > 0.7 and self.glow:
      screen.blit(lower,self.pos)
    if self.life_left > 0.3:
      screen.blit(low,self.pos)
    screen.blit(normal,self.pos)

  def apply_force(self,force,time):
    self.forces.append((force,time,self.life_length))
  def move(self,distance):
    pos_x,pos_y = self.pos
    dis_x,dis_y = distance
    pos_x += dis_x
    pos_y += dis_y
    self.pos = (pos_x,pos_y)
  def update(self,acceleration_down:float,delta_time:float,friction:bool=True,acceleration_right=0):
    self.life_length += delta_time
    self.life_left -= delta_time
    if self.life_length > self.life_time and self.life_time > 0:
      return 'dead'

    a_down = acceleration_down
    a_right = acceleration_right
    for force in self.forces:
      length = force[1]
      start = force[2]
      if self.life_length > length + start:
        self.forces.remove(force)
      else:
        x,y = force[0]
        a_down += y/self.mass
        a_right += x/self.mass

    t = delta_time
    v_down = self.vel[1]
    v_right = self.vel[0]
    if abs(v_right) > 0.25 and friction:
      a_right -= (0.2 * v_right)
    elif friction:
      v_right = 0
    if abs(v_down) > 0.25 and friction:
      a_down -= (0.2 * v_down)
    elif friction and a_down == 0:
      v_down = 0
    delta_d_down = (1/2 * a_down * (t**2)) + (v_down * t)
    delta_d_right = (1/2 * a_right * (t**2)) + (v_right * t)
    dv_right = a_right*t
    v_right += dv_right
    dv_down = a_down*t
    v_down += dv_down
    self.vel = (v_right,v_down)

    self.move((delta_d_right,delta_d_down))
    if self.pos[1] > 400:
      return 'dead'

    self.draw()

def create_particle(pos,vel,col,list_of,life_time = 0,glow = False):
  list_of.append(Particle(pos,vel,col,life_time,glow=glow))
def boom(colours:list,size,fullness,pos,list_of,range_of = 180,life_time = 0,start_angle = 90,glow = False):
  velocities = []
  for i in range(fullness):
    angle = (i)/(fullness / range_of) + start_angle
    angle = rad(angle)
    vel = ((size/2 + round(random.uniform(-size/2,size/2))) * math.cos(angle),size * math.sin(angle))
    velocities.append(vel)
  for vel in velocities:
    colour = choose_random(colours)
    create_particle(pos, vel, colour, list_of,life_time,glow)

class Button:
  def __init__(self,image,name,position = (0,0),do_on_click=None):
    self.image = image
    self.name = name
    self.on_click = do_on_click
    self.pos = position
  def rect(self):
    rect = self.image.get_rect()
    rect.left += self.pos[0]
    rect.top += self.pos[1]
    return rect
  def is_in(self,point):
    image_rect = self.rect()
    return image_rect.collidepoint(point[0], point[1])
  def update(self,mouse_pos=None,clicked = False):
    if clicked:
      if self.on_click != None:
        self.on_click(self)
    if self.is_in(mouse_pos):
      image_rect = self.rect()
      border = pygame.Rect(image_rect.left,image_rect.top,image_rect.width,image_rect.height)
      border.top -= 1
      border.left -= 1
      border.width += 2
      border.height += 2
      pygame.draw.rect(screen,0xffffff,border)
    screen.blit(self.image,self.pos)

screen_size = width, height = (600,400)
fps = 60
background_colour = (0,0,0)
physics_step_duration = 1/fps
physics_sub_steps = 10

pygame.init()
screen = pygame.display.set_mode(screen_size)
low_alpha = pygame.Surface((width,height))
low_alpha.set_colorkey((0,0,0))
low_alpha.set_alpha(80)
lower_alpha = pygame.Surface((width,height))
lower_alpha.set_colorkey((0,0,0))
lower_alpha.set_alpha(40)
clock = pygame.time.Clock()

colours = { #colours available for the snake
  'pink':   0xffafaf,
  'green':  0x00ff00,
  'blue':   0x0000ff,
  'yellow': 0xffff00,
  'cyan':   0x00ffff,
  'magenta':0xff00ff,
  'white':  0xffffff,
  'grey':   0xafafaf,
  }

number_colours = {#colours for the numbers in minesweeper, use rgb because of text
  1:  (0,0,230),
  2:  (0,180,0),
  3:  (255,0,0),
  4:  (223,0,255),
  5:  (150,75,0),
  6:  (0,255,255),
  7:  (0,0,0),
  8:  (208,208,208),
}

white = colours['white']
black = 0x000000
red = 0xff0000

class Keyset:
  def __init__(self,up,right,down,left):
    self.up = up
    self.right = right
    self.down = down
    self.left = left

p1_keys = Keyset(pygame.K_UP,pygame.K_RIGHT,pygame.K_DOWN,pygame.K_LEFT)
p2_keys = Keyset(pygame.K_w,pygame.K_d,pygame.K_s,pygame.K_a)
p3_keys = Keyset(pygame.K_KP_8,pygame.K_KP_6,pygame.K_KP_5,pygame.K_KP_4,)
p4_keys = Keyset(pygame.K_i,pygame.K_l,pygame.K_k,pygame.K_j)

num_keys = {
  pygame.K_1:1,
  pygame.K_2:2,
  pygame.K_3:3,
  pygame.K_4:4,
  pygame.K_5:5,
  pygame.K_6:6,
  pygame.K_7:7,
  pygame.K_8:8,
  pygame.K_9:9,
  pygame.K_0:0,
}

class Grid:
  def __init__(self,c:list):
    self.cols = c
  def get_value(self,x,y):
    """
    gets the value at the specified position in the grid
    """
    try:
      return self.cols[x][y]
    except Exception as ex:
      print(f'x: {x}\ny: {y}\nException: {ex}\n')
  def set_value(self,x,y,value):
    """
    sets the value at the specified position in the grid
    """
    self.cols[x][y] = value
  def get_max(self):
    return (len(self.cols) - 1,len(self.cols[0]) - 1)
  def all_positions(self,dictionary:bool):
    if dictionary:
      positions = {}
    else:
      positions = []
    x = -1
    for collum in self.cols:
      x+=1
      y = -1
      for space in collum:
        y+=1
        if dictionary:
          positions[(x,y)] = self.get_value(x,y)
        else:
          positions.append((x,y))
    return positions

def create_grid(collums:int,rows_int:int,default = 0):
  """
  creates a grid with every value set to default, with a width of collums, and a height of rows
  """
  if collums < 1:
    raise ValueError('collums must be an integer greater than 0')
  if rows_int < 1:
    raise ValueError('rows_int must be an integer greater than 0')

  cols = []
  for i in range(collums):
    row = []
    for i in range(rows_int):
      row.append(default)
    cols.append(row)
  return Grid(cols)

def make_rect_at(x,y,snake:bool):
  top = (y-(1*snake))*20
  left = (x-(1*snake))*20
  width = 20
  height = 20
  return pygame.Rect(left,top,width,height)

def text_to_screen(text, pos, size = 45, color = (255,255,255)):
  text = str(text)
  font = pygame.font.SysFont('blockhead',  size)
  text = font.render(text,True,color)
  screen.blit(text, pos)

def main():
  pygame.display.set_caption('Simpler Games')
  print('hello world!')

  def snake(self):
    global background_colour

    playarea = create_grid(int(width/20) + 2,int(height/20) + 2,0)
    # playarea = create_grid(int(width/20) - 1000,int(height/20) + 2,0)

    #all_positions example
    # all_positions = playarea.all_positions(True)
    # for pos in all_positions:
    #   print(f'position: {pos}\n value: {all_positions[pos]}\n')
    #prints like this:
    #position: (31,16)
    # value: 0
    #
    #position: (31,17)
    # value: 0
    #

    global fps
    fps = 4

    pygame.display.set_caption('Snake')

    mirror_mode = False

    class Player:
      def __init__(self,starting_pos,keys,number):
        self.direction = (0,0)
        self.directions = [self.direction]
        self.snake_positions = [starting_pos]
        self.snake_length = 3
        self.score = 0
        self.snake_colour = (0xffffff)
        self.snake_head = (starting_pos)
        self.next_pos = (0,0)
        self.keys = keys
        self.number = number

    player1 = Player((5,5),p1_keys,1)
    player2 = Player((25,5),p2_keys,2)
    player3 = Player((5,15),p3_keys,3)
    player4 = Player((25,15),p4_keys,4)
    
    num = 0
    while True:
      In = input('how many players do you want to play with?\n')
      try:
        num = int(In)
        if num <= 4 and num >= 1:
          break
        else:
          raise
      except:
        print('please type a valid integer between 1 and 4')
    
    players_list = [
      player1,
      player2,
      player3,
      player4,
    ]

    players = {}
    for i in range(num):
      players[i+1] = players_list[i]
        
    for player in players:
      while True:
        print(f'\nchoose a colour for player {player}. available colours are:')
        for colour in colours:
          print(colour)
        try:
          In = input()
          players[player].snake_colour = colours[In]
          break
        except:
          print('invalid colour. please ensure proper spelling\n')
          
    In = input('type "yes" to enable mirror mode\n')
    if In == 'yes':
      mirror_mode = True
      print('mirror mode enabled')

    def set_walls():
      x = -1
      for col in playarea.cols:
        x += 1
        y = -1
        for row in col:
          y += 1
          if x == 0 or y == 0 or x == width/20 + 1 or y == height/20 + 1: 
            playarea.set_value(x,y,1)

    set_walls()
    main_running = True
    fruit_positions = []
    fruits = 1

    def create_fruit():
      while True:
        x = random.randint(0,width/20)
        y = random.randint(0,height/20)
        if playarea.get_value(x,y) == 0:
          playarea.set_value(x,y,2)
          fruit_positions.append((x,y))
          break

    def add_snake_pos(x,y,player):
      value = playarea.get_value(x,y)
      if value == 1:
        return 'obst'
      else:  
        playarea.set_value(x,y,1)
        player.snake_positions.append((x,y))
        if value == 2:
          fruit_positions.remove((x,y))
          return 'fruit'
        else:
          return 'empty'

    def remove_snake_pos(player):
      x = player.snake_positions[0][0]
      y = player.snake_positions[0][1]
      player.snake_positions.remove((x,y))
      playarea.set_value(x,y,0)

    def update(player):
      for pos in player.snake_positions:
        pygame.draw.rect(screen,player.snake_colour,make_rect_at(pos[0],pos[1],True))
      for pos in fruit_positions:
        pygame.draw.rect(screen,red,make_rect_at(pos[0],pos[1],True))

    game_over = False

    while game_over == False:
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            main_running = True

      while main_running:
        screen.fill(background_colour)
        if len(fruit_positions) < fruits:
          for i in range(fruits-len(fruit_positions)):
            create_fruit()
        #
        for player in players:
          players[player].snake_head = players[player].snake_positions[len(players[player].snake_positions)-1]

        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            main_running = False
          elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
              print('clicky')
          elif event.type == pygame.KEYDOWN:
            for player in players:
              if event.key == players[player].keys.up:
                if players[player].direction != (0,1) or len(players[player].directions) > 1:
                  players[player].directions.append((0,-1))
                  if players[player].direction == (0,0):
                    players[player].direction = (0,-1)
                    players[player].directions.remove((0,0))
              elif event.key == players[player].keys.down:
                if players[player].direction != (0,-1) or len(players[player].directions) > 1:
                  players[player].directions.append((0,1))
                  if players[player].direction == (0,0):
                    players[player].direction = (0,1)
                    players[player].directions.remove((0,0))
              elif event.key == players[player].keys.right:
                if players[player].direction != (-1,0) or len(players[player].directions) > 1:
                  players[player].directions.append((1,0))
                  if players[player].direction == (0,0):
                    players[player].direction = (1,0)
                    players[player].directions.remove((0,0))
              elif event.key == players[player].keys.left:
                if players[player].direction != (1,0) or len(players[player].directions) > 1:
                  players[player].directions.append((-1,0))
                  if players[player].direction == (0,0):
                    players[player].direction = (-1,0)
                    players[player].directions.remove((0,0))
            if event.key == pygame.K_ESCAPE:
              main_running = False
            elif event.key == pygame.K_SPACE:
              main_running = False
            else:
              for key in num_keys:
                if event.key == key:
                  fps = num_keys[key]

        for player in players:
          if players[player].directions[0] != players[player].direction or len(players[player].directions) == 1:
            players[player].direction = players[player].directions[0]
          else:
            players[player].direction = players[player].directions[1]
          players[player].next_pos = (players[player].snake_head[0] + players[player].direction[0], players[player].snake_head[1] + players[player].direction[1])
          if mirror_mode:
            if players[player].next_pos[0] > playarea.get_max()[0] - 1:
              players[player].next_pos = (1,players[player].next_pos[1])
            elif players[player].next_pos[0] < 1:
              players[player].next_pos = (playarea.get_max()[0]-1,players[player].next_pos[1])
            if players[player].next_pos[1] > playarea.get_max()[1] - 1:
              players[player].next_pos = (players[player].next_pos[0],1)
            elif players[player].next_pos[1] < 1:
              players[player].next_pos = (players[player].next_pos[0],playarea.get_max()[1]-1)
            
          while True:
            if len(players[player].directions) > 1:
              players[player].directions.remove(players[player].directions[0])
            else:
              break
          if len(players[player].snake_positions) >= players[player].snake_length:
            remove_snake_pos(players[player])
          if players[player].direction != (0,0):
            att = add_snake_pos(players[player].next_pos[0],players[player].next_pos[1],players[player])
            if att == 'fruit':
              players[player].snake_length += 1
              players[player].score += 1
            elif att == 'obst':
              #lost
              print(f'player {player} hit an obstacle. player {player} loses.')
              for playerA in players:
                print(f'player {playerA} score: {players[playerA].score}')
              game_over = True
              main_running = False
        #
        text_to_screen(str(player1.score),(width/3-15,40))
        if len(players) > 1:
          text_to_screen(str(player2.score),(2*width/3-15,40))
        if len(players) > 2:
          text_to_screen(str(player3.score),(width/3-15,height-40))
        if len(players) > 3:
          text_to_screen(str(player4.score),(2*width/3-15,height-40))
        for player in players:
          update(players[player])
        pygame.display.flip()
        pygame.display.update()
        clock.tick(fps)
    pygame.display.set_caption('Menu')
#---------------------------------------------------------------------------
  def minesweeper(self):
    global fps
    fps = 60
    pygame.display.set_caption('Minesweeper')
    playarea = create_grid(int(width/20),int(height/20),0)

    revealed = {}
    flagged = []

    def change_pix_to_pos(pix:int):
      pos_x = math.floor(pix[0]/20)
      pos_y = math.floor(pix[1]/20)
      return (pos_x,pos_y)
    def change_pos_to_pix(pos:int,centred:bool):
      pix_x = pos[0]*20
      pix_y = pos[1]*20
      if centred:
        pix_x+=10
        pix_y+=10
      return (pix_x,pix_y)

    bombs_list = []

    def make_bombs(bombs:int,unallowed:list,forced:list):
      for i in range(bombs):
        while True:
          if forced == []:
            x = random.randint(0,29)
            y = random.randint(0,19)
            if (x,y) not in bombs_list and (x,y) not in unallowed:
              bombs_list.append((x,y))
              playarea.set_value(x,y,1)
              break
          else:
            x = forced[0][0]
            y = forced[0][1]
            del forced[0]
            if (x,y) not in bombs_list and (x,y) not in unallowed:
              bombs_list.append((x,y))
              playarea.set_value(x,y,1)
              break

    
    def get_bombs_for(x,y):
      if playarea.get_value(x,y) == 1:
        return 'bomb'
      else:
        bombs = 0
        for a in range(-1,2):
          for b in range(-1,2):
            if a != 0 or b != 0:
              if ((x >= 1 and x <= 28) or (x == 0 and a > -1) or (x == 29 and a < 1)) and ((y >= 1 and y <= 18) or (y == 0 and b > -1) or (y == 19 and b < 1)):
                if playarea.get_value(x+a,y+b) == 1:
                  bombs+=1
        return bombs
    
    def check_around(x,y,include):
      middle = get_bombs_for(x,y)
      if middle == 'bomb' and include:
        print('that was a bomb')
        return 'lose'
      else:
        if include and type(middle) == type(0+1):
          revealed[x,y] = middle
        if middle == 0:
          for a in range(-1,2):
            for b in range(-1,2):
              if a != 0 or b != 0:
                if ((x >= 1 and x <= 28) or (x == 0 and a > -1) or (x == 29 and a < 1)) and ((y >= 1 and y <= 18) or (y == 0 and b > -1) or (y == 19 and b < 1)):
                  pos = (x+a,y+b)
                  bombs = get_bombs_for(pos[0],pos[1])
                  if bombs == 0:
                    if pos not in revealed:
                      revealed[pos] = bombs
                      check_around(pos[0],pos[1],False)
                  elif bombs != 'bomb':
                    if pos not in revealed:
                      revealed[pos] = bombs
        return 'stay'
    clicks = 0
    running = True
    colour_test = False
    t = 0
    time_started = False

    while running:
      dt = clock.get_time()/1000
      if time_started:
        t += dt
      for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
          pos = change_pix_to_pos(event.pos)
          if event.button == 1:
            if pos not in flagged:
              if clicks == 0:
                time_started = True
                forced = []
                unallowed = [(0,0)]
                unallowed.append(pos)
                x = pos[0]
                y = pos[1]
                for a in range(-1,2):
                  for b in range(-1,2):
                    if a != 0 or b != 0:
                      if ((x >= 1 and x <= 28) or (x == 0 and a > -1) or (x == 29 and a < 1)) and ((y >= 1 and y <= 18) or (y == 0 and b > -1) or (y == 19 and b < 1)):
                        unallowed.append((x+a,y+b))
                make_bombs(71,unallowed,forced)
                bombs_list.sort()

              if pos not in revealed:
                a = check_around(pos[0],pos[1],True)
                if a == 'lose':
                  print('you lost')
                  running = False
              clicks += 1
          elif event.button == 2:
            colour_test = not colour_test
          elif event.button == 3:
            if pos not in flagged:
              bisect.insort(flagged,pos)
            else:
              flagged.remove(pos)
            if flagged == bombs_list and len(bombs_list) > 0:
              print('you won')
              running = False
      positions = playarea.all_positions(False)
      for pos in positions:
        if pos not in revealed and pos not in flagged:
          pygame.draw.rect(screen,0x00ff00,make_rect_at(pos[0],pos[1],False))
      for flag in flagged:
        pygame.draw.rect(screen,0xff0000,make_rect_at(flag[0],flag[1],False))
      for pos in revealed:
        bombs = revealed[pos]
        pygame.draw.rect(screen,0xffffff,make_rect_at(pos[0],pos[1],False))
        if bombs != 0:
          colour = number_colours[bombs]
          text_to_screen(str(bombs),change_pos_to_pix(pos,False),34,colour)
      if colour_test:
        for number in rainbow:
          colour = number
          pygame.draw.rect(screen,colour,make_rect_at(number,1,False))
        for i in range(1,6):
          pygame.draw.rect(screen,rainbow[i],make_rect_at(i,2,False))
      text_to_screen(str(round(t)) + 's',((width/2) - 20,15),color=(0,0,0))
      clock.tick()
      pygame.display.flip()
      pygame.display.update()
    pygame.display.set_caption('Menu')
#------------------------------------------------------------------------
  def physics(self):
    while True:
      try:
        In = input('what is your rpm (int)')
        rpm = int(In)
        break
      except:
        print('bad input. input was ' + In)

    while True:
      try:
        In = input('what is your angle (int)')
        angle = int(In)
        break
      except:
        print('bad input. input was ' + In)

    while True:
      try:
        In = input('what is your height of release (float)')
        height_of = float(In)
        break
      except:
        print('bad input. input was ' + In)
    f = rpm/60
    vel = 2 * math.pi * height_of * f
    vel_x = vel * abs(math.cos(rad(angle)))
    vel_y = vel * abs(math.sin(rad(angle)))

    print(str(vel) + 'm/s')
    print('(' + str(vel_x) + ', ' + str(vel_y) + ') m/s')
    t = 0
    if height_of == 0:
      t = (2* vel_y) / 9.81
    else:
      t = ((vel_y + (math.sqrt(((vel_y)*(vel_y)) - (2*-9.81*height_of))))/9.81)
    print(str(t) + 's')
    dist = vel_x * t
    print(str(dist) + 'm')
    pygame.display.set_caption('Menu')
#----------------------------------------------------------------------------------
  def simon(self):
    pygame.display.set_caption('Simon')
    print("press 'm' to mute")
    global fps
    fps = 60              
    frames = 0
    mouse_pos = (0,0)
    flash_time = 0.3
    muted = False

    class Simon_Rect:
      def __init__(self,rect,colours,tone_pitch,name):
        self.rect = rect
        self.centre = (rect.top - rect.height/2,rect.left - rect.width/2)
        self.colours = colours
        self.colour = colours[0]
        self.flashing = False
        self.flash_start = 0
        self.pitch = tone_pitch
        self.name = name
      def flash(self,time_started):
        self.flash_start = time_started
        self.flashing = True
      def is_in(self,point):
        return self.rect.collidepoint(point[0], point[1])
      def update(self,time,mouse_pos):
        if self.flashing:
          if time > self.flash_start + flash_time:
            self.flashing = False
            self.colour = self.colours[0]
          else:
            self.colour = self.colours[1]
        else:
          self.colour = self.colours[0]
        if self.is_in(mouse_pos):
          border = pygame.Rect(self.rect.left,self.rect.top,self.rect.width,self.rect.height)
          border.top -= 1
          border.left -= 1
          border.width += 2
          border.height += 2
          pygame.draw.rect(screen,0xffffff,border)
        pygame.draw.rect(screen,self.colour,self.rect)


    dist_from = 40

    def make_simon_rect(down,right,colours,tone_pitch,name):
      left = dist_from
      top = dist_from
      wid = width/2 - dist_from - 1
      hei = height/2 - dist_from - 1
      if down:
        top = top + hei + 2
      if right:
        left = left + wid + 2
      return Simon_Rect(pygame.Rect(left,top,wid,hei),colours,tone_pitch,name)
      
    top_left = make_simon_rect(False,False,[0xdf0000,0xff0000],1500,'red rectangle')
    top_right = make_simon_rect(False,True,[0x00df00,0x00ff00],1250,'green rectangle')
    bot_left = make_simon_rect(True,False,[0xdfdf00,0xffff00],1000,'yellow rectangle')
    bot_right = make_simon_rect(True,True,[0x0000df,0x0000ff],750,'blue rectangle')
    
    rectangles = [top_left,top_right,bot_left,bot_right]

    pattern = []
    time_between_pattern_show = 1.5
    pattern_went_time = 0
    def add_to_pattern(t):
      pattern.append(choose_random(rectangles))
      pattern_went_time = t

    choices = []
    player_started = False
    flashed = 0
    time_between_flashes = 0.2
    flashes_start = 0

    def get_flashing():
      list = []
      for rect in rectangles:
        if rect.flashing:
          list.append(rect)
      return list

    running = True
    t = 0 #time since start in seconds
    add_to_pattern(t)
    while running:
      screen.fill(background_colour)
      frames += 1
      dt = clock.get_time()/1000
      t+= dt 

      if t - pattern_went_time > time_between_pattern_show and player_started == False:
        for i in range(len(pattern)):
          if len(get_flashing()) > 0 or t - flashes_start < flash_time + time_between_flashes:
            break
          elif flashed == len(pattern):
            pattern_went_time = t
            flashed = 0
          elif flashed == i:
            flashed += 1
            flashes_start = t
            flashing_rect = pattern[i]
            flashing_rect.flash(t)
            # if not muted:
            #   play_tone(flash_time,flashing_rect.pitch,flashing_rect.name + ' tone')                   
      next_to_click = pattern[len(choices)]
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
          running = False
        elif event.type == pygame.MOUSEMOTION:
          mouse_pos = pygame.mouse.get_pos()
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_m:
            muted = not muted
        elif event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
            for rect in rectangles:
              if rect.is_in(mouse_pos):
                if player_started == False:
                  player_started = True
                choices.append(rect)
                if rect != next_to_click:
                  print('you lose. score: ' + str(len(pattern)- 1))
                  running = False
                if len(choices) == len(pattern):
                  add_to_pattern(t)
                  choices = []
                  player_started = False
                  pattern_went_time = t
                
                rect.flash(t)       
                # if not muted:
                #   play_tone(flash_time,rect.pitch,rect.name + ' tone')

      text_to_screen(str(len(pattern)- 1),(width/2,10))
      for rect in rectangles:
        rect.update(t,mouse_pos)
      clock.tick()
      pygame.display.flip()
      pygame.display.update()
    pygame.display.set_caption('Menu')
#---------------------------------
  def test(self):
    pygame.display.set_caption('Test')
    print('testing')

    button_img = pygame.image.load('button_image.png')
    print(button_img.get_rect())
    running = True
    def button_on_click(self):
      nonlocal running
      print(self.name + ' was clicked!')
      running = False
    
    buttons = []
    test_button = Button(button_img,'test button',(20,20),button_on_click)
    buttons.append(test_button)
    mouse_pos = (0,0)
    t = 0
    particles = []
    paused = False



    while running:
      screen.fill(background_colour)
      low_alpha.fill((0,0,0))
      dt = clock.get_time()/1000
      t+= dt 
      for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
          mouse_pos = pygame.mouse.get_pos()
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            paused = not paused
        elif event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
            In = False
            for button in buttons:
              if button.is_in(event.pos):
                button.update(mouse_pos,clicked=True)
                In = True
            if not In:
              boom([(0,255,0),(255,0,0),(255,255,0)],30,180,mouse_pos,particles,360,5)
      for button in buttons:
        button.update(mouse_pos)
      if not paused:
        for particle in particles:
          if particle.update(g,dt) == 'dead':
            particles.remove(particle)
      else:
        for particle in particles:
          particle.draw()
      screen.blit(low_alpha,(0,0))
      clock.tick()
      pygame.display.flip()
      pygame.display.update()
    pygame.display.set_caption('Menu')
    #--------------------------------------------------------FIREWORKS

  def fireworks(self):
    pygame.display.set_caption('Fireworks')

    button_img = pygame.image.load('exit_button.png')
    running = True
    def button_on_click(self):
      nonlocal running
      running = False

    instructions = [
      '',
      'left click on the screen to create a firework',
      'scroll up or down to change the size of fireworks',
      'press space to pause or unpause the game',
      'right click to remove all fireworks',
      "hold 'q' while dragging to move the fireworks",
      "press 'r' to make the fireworks rainbow",
      'hold control while scrolling to change how many particles in a firework',
      'hold shift while scrolling to change the time the fireworks last',
      'hold shift and control while scrolling to change gravity',
      "press 'g' to change how much glow there is",
      'Have fun!',
    ]
    def print_controls(self):
      for instruction in instructions:
        print(instruction)
    buttons = []
    exit_button = Button(button_img,'exit button',(20,20),button_on_click)
    controls_button = Button(pygame.image.load('controls_button.png'),'controls button', (20,60),print_controls)

    buttons.append(exit_button)
    buttons.append(controls_button)

    time_between_forces = 1/5
    last_force = -time_between_forces

    mouse_pos = (0,0)
    t = 0
    particles = []
    paused = False
    size = 30
    max_size = 100
    max_full = 100
    fullness_offset = 30
    fullness = size * 7
    rainbows = False
    time_alive = 22.5
    max_time = 225
    gravity = 30
    max_gravity = 100
    glow = False

    ctrl_down = False
    shift_down = False
    q_down = False
    mouse_down = False
    gry = [(0,255,0),(255,0,0),(255,255,0)]

    class MovingImage:
      def __init__(self,image,pos,vel):
        self.image = image
        self.pos = pos
        self.vel = vel
      def draw(self):
        screen.blit(self.image,self.pos)
      def move(self,dist):
        x,y = dist
        self.pos = (self.pos[0] + x,self.pos[1] + y)
      def update(self,dt):
        vel_x,vel_y = self.vel
        dist_x = vel_x * dt
        dist_y = vel_y * dt
        self.move((dist_x,dist_y))
        if (0 > self.pos[0] or self.pos[0] > width) or (0 > self.pos[1] or self.pos[1] > height):
          return 'dead'
        self.draw()

    horses_list = []
    horse_img = pygame.image.load('horse_image.jpg')
    horse_img = pygame.transform.scale(horse_img,(50,50))

    def make_horse():
      horses_list.append(MovingImage(horse_img,(0,height/2),(100,0)))

    def firework_boom():
      if not rainbows:
        boom(gry,size-1,fullness,mouse_pos,particles,360,(time_alive/5),0,glow)
      else:
        boom(rainbow,size-1,fullness,mouse_pos,particles,360,(time_alive/5),0,glow)


    while running:
      screen.fill(background_colour)
      low_alpha.fill((0,0,0))
      lower_alpha.fill((0,0,0))
      dt = clock.get_time()/1000
      fullness = int(size * ((fullness_offset/5) + math.floor(size/30)))

      for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
          if mouse_down and q_down:
            x2,y2 = pygame.mouse.get_pos()
            x1,y1 = mouse_pos
            x = (x2-x1)
            y = (y2-y1)
            dist = (x,y)
            for particle in particles:
              particle.move(dist)
            for horse in horses_list:
              horse.move(dist)
            
          mouse_pos = pygame.mouse.get_pos()
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            paused = not paused
          elif event.key == pygame.K_r:
            rainbows = not rainbows
          elif event.key == pygame.K_g:
            glow = not glow
          elif event.key == pygame.K_b:
            bluescreen('hello')
          elif event.key == pygame.K_h:
            make_horse()
          elif event.key == pygame.K_LCTRL:
            ctrl_down = True
          elif event.key == pygame.K_q:
            q_down = True
          elif event.key == pygame.K_LSHIFT:
            shift_down = True
        elif event.type == pygame.KEYUP:
          if event.key == pygame.K_LCTRL:
            ctrl_down = False
          elif event.key == pygame.K_LSHIFT:
            shift_down = False
          elif event.key == pygame.K_q:
            q_down = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
            mouse_down = True
            In = False
            for button in buttons:
              if button.is_in(event.pos):
                button.update(mouse_pos,clicked=True)
                In = True
            if not In and not q_down:
              firework_boom()
          elif event.button == 3:
            particles.clear()
          elif event.button == 4:
            if not ctrl_down and not shift_down:
              if size < max_size:
                size += 5
            elif shift_down and not ctrl_down:
              if time_alive < max_time:
                time_alive += 2.5
            elif shift_down and ctrl_down:
              if gravity < max_gravity:
                gravity += 5
            else:
              if fullness_offset < max_full:
                fullness_offset += 5
          elif event.button == 5:
            if not ctrl_down and not shift_down:
              if size > 5:
                size -= 5
            elif shift_down and not ctrl_down:
              if time_alive > 2.5:
                time_alive -= 2.5
            elif shift_down and ctrl_down:
              if gravity > -100:
                gravity -= 5
            else:
              if fullness_offset > 5:
                fullness_offset -= 5
        elif event.type == pygame.MOUSEBUTTONUP:
          if event.button == 1:
            mouse_down = False

      text_to_screen(f'size: {size}',(10,100 + 16 * 0),20)
      text_to_screen(f'fullness: {fullness_offset}',(10,100 + 16 * 1),20)
      text_to_screen(f'life time: {time_alive}',(10,100 + 16 * 2),20)
      text_to_screen(f'gravity: {gravity}',(10,100 + 16 * 3),20)

      m = 0
      if t >= 60:
        m = math.floor(t/60)

      text_to_screen(f'time: {m}m {round(t - (m*60),1)}s',(10,100 + 16 * 4),20)
      if rainbows:
        text_to_screen(f'colour: rainbow',(10,100 + 16 * 5),20)
      else:
        text_to_screen(f'colour: normal',(10,100 + 16 * 5),20)
      if glow:
        text_to_screen(f'glow: extra',(10,100 + 16 * 6),20)
      else:
        text_to_screen(f'glow: normal',(10,100 + 16 * 6),20)
        
      if not paused:
        t+= dt 
      for button in buttons:
        button.update(mouse_pos)
      if not paused:
        for particle in particles:
          if particle.update(gravity/3,dt) == 'dead':
            particles.remove(particle)
        if len(particles) > 0 and t-last_force > time_between_forces:
          particle = choose_random(particles)
          particle.apply_force((0.01,0),particle.life_left)
          particle.apply_force((-0.01,0),particle.life_left)
          last_force = t
        for horse in horses_list:
          if horse.update(dt) == 'dead':
            horses_list.remove(horse)
      else:
        for particle in particles:
          particle.draw()
      if paused:
        for horse in horses_list:
          horse.draw()
      screen.blit(low_alpha,(0,0))
      screen.blit(lower_alpha,(0,0))
      clock.tick()
      pygame.display.flip()
      pygame.display.update()
    pygame.display.set_caption('Menu')
#-----------------------------------------------------------
  def start_code(self):
    pygame.display.set_caption('starting code')
    button_img = pygame.image.load('exit_button.png')

    running = True
    t = 0

    def button_on_click(self):
      nonlocal running
      running = False

    buttons = []
    exit_button = Button(button_img,'exit button',(20,20),button_on_click)

    buttons.append(exit_button)
    mouse_pos = (0,0)

    while running:
      screen.fill(background_colour)
      dt = clock.get_time()/1000
      t+=dt
      for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
          mouse_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
            for button in buttons:
              if button.is_in(event.pos):
                button.update(mouse_pos,clicked=True)

      for button in buttons:
        button.update(mouse_pos)

      clock.tick()
      pygame.display.flip()
      pygame.display.update()
    pygame.display.set_caption('Menu')
#-----------------------------------------------------------

  def bluescreen(self):
    pygame.display.set_caption('blue screen')
    running = True
    while running:
      screen.fill(0x0000ff)
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            running = False
      clock.tick()
      pygame.display.flip()
      pygame.display.update()
    pygame.display.set_caption('Menu')

  def story_time(self):
    def get_inp(prompt,blacklist:list=None,whitelist:list=None):
      while True:
        In = input(f'{prompt}\n')
        if whitelist != None:
          if In in whitelist:
            return In
          else:
            print('invalid input. input was: ' + In)
        elif blacklist != None:
          if In not in blacklist:
            return In
          else:
            print('invalid input. input was: ' + In)
        else:
          return In
    get_inp('say hi',whitelist=['hi'])
    print('nah bye lol')
#-----------------------------------------------------------
  def gravity_simulator(self):
    pygame.display.set_caption('gravity')
    button_img = pygame.image.load('exit_button.png')

    running = True
    t = 0

    pix_size = 1000#metres

    def button_on_click(self):
      nonlocal running
      running = False

    class Body:
      def __init__(self,mass:float,radius:int,position:tuple,velocity:tuple=0):
        self.mass = mass
        self.radius = radius
        self.pos = position
        self.vel = velocity

      def energy_to_vel(self,energy):
        return math.sqrt((2*energy)/self.mass)

      def apply_energy(self,energy:tuple):
        E_x,E_y = energy
        v_x,v_y = self.vel
        v_x += self.energy_to_vel(E_x)
        v_y += self.energy_to_vel(E_y)
        self.vel = (v_x,v_y)
      
      def update(self,dt,g):
        pass

    buttons = []
    exit_button = Button(button_img,'exit button',(20,20),button_on_click)

    buttons.append(exit_button)
    mouse_pos = (0,0)

    while running:
      screen.fill(background_colour)
      dt = clock.get_time()/1000
      t+=dt
      for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
          mouse_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
            for button in buttons:
              if button.is_in(event.pos):
                button.update(mouse_pos,clicked=True)

      for button in buttons:
        button.update(mouse_pos)

      clock.tick()
      pygame.display.flip()
      pygame.display.update()
    pygame.display.set_caption('Menu')

#----------------------------------------------------------------

  def get_dist(p1,p2):
    return math.sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))

  def touching(point_1:tuple,point_2:tuple):
    if get_dist(point_1,point_2) > 1:
      return False
    else:
      return True

  while True:
    pygame.display.set_caption('Menu')
    snake_button = Button(pygame.image.load('snake_button.png'),'snake',(50,10),snake)
    minesweeper_button = Button(pygame.image.load('minesweeper_button.png'),'mine_sweeper',(50,50),minesweeper)
    simon_button = Button(pygame.image.load('simon_button.png'),'simon',(50,130),simon)
    phys_button = Button(text_to_img('story'),'phys',(300,300),story_time)
    test_button = Button(pygame.image.load('test_button.png'),'test',(500,300),test)
    fireworks_button = Button(pygame.image.load('fireworks_button.png'),'fireworks',(50,180),fireworks)
    blue_button = Button(pygame.image.load('blue_button.png'),'blue',(50,240),bluescreen)
    buttons = [
      snake_button,
      minesweeper_button,
      simon_button,
      phys_button,
      test_button,
      fireworks_button,
      blue_button
    ]

    mouse_pos = (0,0)


    draw_layer = pygame.Surface((width,height))
    draw_layer.fill(background_colour)
    draw_layer.set_colorkey(background_colour)
    mouse_down = False

    running = True
    while running:
      screen.fill(background_colour)
      for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
          prev_pos = mouse_pos
          mouse_pos = pygame.mouse.get_pos()
          if mouse_down:
            pygame.draw.line(draw_layer,0xffffff,prev_pos,mouse_pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
            mouse_down = True
            in_button = False
            for button in buttons:
              if button.is_in(event.pos):
                button.update(mouse_pos,clicked=True)
                in_button == True
          elif event.button == 3:
            draw_layer.fill(background_colour)
        elif event.type == pygame.MOUSEBUTTONUP:
          if event.button == 1:
            mouse_down = False

      screen.blit(draw_layer,(0,0))
      for button in buttons:
        button.update(mouse_pos)
      clock.tick()
      pygame.display.flip()
      pygame.display.update()

    


if __name__ == '__main__':
  main()