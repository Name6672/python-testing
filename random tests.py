

import random
import timeit

def make_random():
  number = random.randrange(0,1e69)
  return number

numbers = []
for i in range(1000):
  numbers.append(make_random())

def get_max(li):
  max = li[0]
  for number in li:
    if number > max:
      max = number
  return max
def main():
  print(max(numbers))
  
if __name__ == '__main__':
  main()