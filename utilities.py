import pygame
import math
from pymunk.vec2d import Vec2d
import random

#-------------------------------Utilities-------------------------------

def random_true_or_false():
  return bool(random.randint(0,1))

def is_border(x,y,x_max,y_max):
  return (y == 0 or x == 0 or y == (y_max - 1) or x == (x_max - 1))

def text_to_screen(screen, text, pos, size = 30, color = (255, 255, 255), font = 'timesnewroman',background = False):
  """
  Print some text to a screen. Specifying size is unnecessary if you specify the font as a pygame font and not a string
  """
  text = str(text)
  if type(font) == str:
    font = pygame.font.SysFont(font,  size)
  if background:
    text_back = font.render(text,True,(0,0,0))
    offset = Vec2d(0,0)
    for i in range(4):
      if i == 1:
        offset = Vec2d(1,0)
      elif i == 2:
        offset = Vec2d(0,1)
      elif i == 3:
        offset = Vec2d(-1,0)
      elif i == 4:
        offset = Vec2d(0,-1)
        print('it works')
    pos_w_off = Vec2d(pos[0]+offset[0],pos[1]+offset[1])
    screen.blit(text_back,pos_w_off)
  text = font.render(text, True, color)
  screen.blit(text, pos)

def is_even(num, mode = True):
  """
  Check if a number is even. set mode to False to check if the number is odd
  """
  if num % 2 == 0:
    return mode
  else:
    return not mode


def to_degrees(radians):
  """
  Convert radians to degrees
  """
  return -(radians / (3.14159))*180

def to_radians(degrees):
  """
  Covert degrees to radians
  """
  return -(degrees / 180) * 3.14159

def dist(p1,p2,vec = False):
  """
  Get the distance between two points. Set vec to True to return a vector
  """
  a = abs(p1[0]-p2[0])
  b = abs(p1[1] - p2[1])
  c = math.sqrt(a+b)
  if vec:
    return Vec2d(a,b)
  else:
    return c

def inc_with_limit(number,increment,limit):
  """
  Increase a number by an limit. If the result is greater than the limit, returns the limit. Otherwise returns the result
  """
  number += increment
  if number > limit:
    number = limit
  return number

def dec_with_limit(number,increment,limit):
  """
  Decreases a number by an increment. If the result is less than the limit, returns the limit. Otherwise returns the result
  """
  number -= increment
  if number < limit:
    number = limit
  return number

def Vec2d_abs(Vec):
  """
  Returns a vector of the absolute values of an input vector
  """
  x = abs(Vec[0])
  y = abs(Vec[1])
  return Vec2d(x,y)

def Vec2d_multiply(vec,coef):
  """
  Multiply a vector by a number or another vector. Works with tuples but always returns a vector
  """
  if type(coef) == Vec2d or type(coef) == tuple:
    x = vec[0] * coef[0]
    y = vec[1] * coef[1]
    return Vec2d(x,y)
  else:
    x = vec[0] * coef
    y = vec[1] * coef
    return Vec2d(x,y)

def Vec2d_avg(list):
  """
  Returns the average of a list of Vectors
  """
  x = 0
  y = 0
  for Vec in list:
    x += Vec[0]
    y += Vec[1]
  try:
    x /= len(list)
    y /= len(list)
  except ZeroDivisionError:
    x = 200
    y = 100
  return Vec2d(x,y)
  