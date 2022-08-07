import pygame
import utilities 

#globals
screen_size = width, height = (600,400)
fps = 60
background_colour = 0x000000
pygame.init()
screen = pygame.display.set_mode(screen_size)

clock = pygame.time.Clock()


def main():
  
  t = 0
  ticks = 0
  mouse_pos = (0,0)
  
  running = True
  while running:
    screen.fill(background_colour)
    utilities.text_to_screen(screen,'Hello, World!',(width/2,height/2),background=True,size=100)
    dt = clock.get_time()/1000
    t+=dt
    for event in pygame.event.get():
      if event.type == pygame.MOUSEMOTION:
        mouse_pos = pygame.mouse.get_pos()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          print('clicky')
          
    pygame.display.flip()
    pygame.display.update()
    ticks += 1
    clock.tick(fps)
  
  print('exiting main')
  
if __name__ == '__main__':
  main()