from ast import arg


class Operation:
  def __init__(self,code,type,arguments,machine_code):
    self.code = code
    self.type = type
    self.arguments = arguments
    self.machine_code = machine_code
    
    
operations = [
  Operation('for','iter',3,[0b])
]

def parse_to_words(filename):
  words = []
  with open(filename,'r') as file:
    content = file.readlines() # seperate file into lines
    
    parsed_lines = [] # list of all lines after parsing
    for line in content: # read each line
      line_words = [] # list of usable strings in the line
      current_word = '' # string being worked with
      
      for char in line: # read each character
        if char != ' ':
          current_word += char
        else:
          line_words.append(current_word)
          current_word = ''
      line_words.append(current_word)
          
      parsed_lines.append(line_words) # add line to parsed lines
  return parsed_lines
    

def main():
  
  filename = ''
  while True:
    try:
      file = None
      filename = input('please enter a filename\n')
      file = open(filename,'r')
      file.close()
      break
    except:
      print('invalid filename. ensure .txt is included at the end')
      
  lines = parse_to_words(filename)
  print(lines)
  
  for line in lines:
    operation = line[0]
    
    
      
      



if __name__ == "__main__":
  main()