#import required libraries
import tkinter as tk
import pygame



#main function standard python stuff
def main():
  
#define variables
  presses = 0
  name = ''

#create window
  root = tk.Tk()
  root.title('hello')
  
#add label
  message = tk.Label(root,text='What is your name?')
  message.pack()
  
#add name entry
  name_string_var = tk.StringVar()
  name_entry = tk.Entry(root,textvariable=name_string_var)
  name_entry.pack()
  
#button press function
  def name_confirmed():
    nonlocal name
    name = name_string_var.get()
    message['text'] = f'Hello, {name}!'
    confirm_button['command'] = button_pressed
    name_entry.pack_forget()
    
  def button_pressed():
    nonlocal presses
    presses+=1
    message['text'] = f'Pressed {presses} {"times!" if presses != 1 else "time!"}'
  
#add button
  confirm_button = tk.Button(root,text='Ok',command=name_confirmed)
  confirm_button.pack()
  
#run window
  root.mainloop()
#print to console when main ends
  print('exiting main')
  
  
#standard python stuff
if __name__ == '__main__':
  main()
else:
  print('opened file as not main')