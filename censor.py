censors = '||'


def censor():
  message = input('enter the message you would like to censor\n')
  new_string = ''
  for char in message:
    new_string += (censors + char + censors)
  return new_string

if __name__ == '__main__':
  with open('output.txt','w') as file:
    file.write(censor())
  