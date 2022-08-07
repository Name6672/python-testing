from BigList import big_list
from PrintAllFunction import print_all

def main():
  In = input('yes or no?\n').lower()
  if In == 'yes':
    print('good!')
  elif In == 'no':
    print('fine >:(')
  elif In == 'list time!':
    print(big_list)
  else:
    print('*murders you murderously*')
    
  print('obligatory hello world:')
  print('Hello, World!')
  
  print('exiting main')

if __name__ == '__main__':
  main()
else:
  print('wtf happened')