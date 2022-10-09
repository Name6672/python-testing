

from textwrap import fill
from turtle import width


class Matrix:
  def __init__(self,height,width,fill_value=0):
    self.height = height
    self.width = width
    self.matrix = self.create_matrix(fill_value)
  def create_matrix(self,fill_value=0):
    matrix = []
    for i in range(self.height):
      col = []
      for b in range(self.width):
        col.append(fill_value)
      matrix.append(col)
    return matrix
  def set_at(self,y,x,value):
    self.matrix[y][x] = value
  def get_at(self,y,x):
    return self.matrix[y][x]
  
  def row_reduce(self):
    col_leads = []
    height_index = 0
    for x in range(self.width):
      for y in range(self.height):
        if self.get_at(y,x) != 0:
          height_index += 1
          