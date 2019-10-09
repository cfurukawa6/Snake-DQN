import random
import pygame
from pygame.locals import *
import time


#use a list of (x,y) to represent snake
class snake():
  #               +x (r), -x (l), +y (u), -y (d)
  __facing_options=[(1,0),(-1,0),(0,1),(0,-1)]

  def __init__(self,x_range,y_range):
    self.snake_list = [(random.randint(0,x_range),random.randint(0,y_range))]  #initializes starting position
    ran = random.randint(0, 3)#(1,0) means facing +x direction
    self.facing = self.__facing_options[ran] #initialize random facing
    self.got_apple = False

  ## WILL CONTROL HEAD OF SNAKE (REST OF BODY IS CONTROLLED BELOW)
  def apply_action(self,*args):
    '''find out what direction the snake will be facing after the action and move snake once'''
    #for *immediate movement
    if args:
      #print("HERE")
      if args[0] =='left':
        if self.facing[0] == 0: #originally moving in +/-y direction  
          self.facing = self.facing[::-1]
          self.facing = (-self.facing[0],self.facing[1])
        else: #originally moving in +/-y direction
          self.facing = self.facing[::-1]

      elif args[0] =='right':
        if self.facing[0] == 0:
          self.facing = self.facing[::-1]
        else:
          self.facing = self.facing[::-1]
          self.facing = (-self.facing[0],self.facing[1])
  
    #detecting movement when snake is constantly moving forward
    else:
      for event in pygame.event.get():
        #cole added (7/31/19)
        if event.type == pygame.QUIT:
          pygame.quit()
        # 
        #keys = pygame.key.get_pressed()
        if event.type == KEYDOWN:
          '''
          if event.key == pygame.K_RIGHT:#keys[pygame.K_LEFT]:
            if self.facing[0] == 0: #originally moving in +/-y direction  
              self.facing = self.facing[::-1]
              self.facing = (-self.facing[0],self.facing[1])
            else: #originally moving in +/-y direction
              self.facing = self.facing[::-1]

          elif event.key == pygame.K_LEFT:#keys[pygame.K_RIGHT]:
            if self.facing[0] == 0:
              self.facing = self.facing[::-1]
            else:
              self.facing = self.facing[::-1]
              self.facing = (self.facing[0],-self.facing[1])
          '''

          #Cole added (7/31)
          #facing = (1,0), (-1,0), (0,1), (0,-1)
          if event.key == pygame.K_LEFT: 
            print('left')
            #checing if facing vertical direction (if not nothing happens) 
            if self.facing[1] == 1: 
              self.facing = self.facing[::-1] #flips tuple
              self.facing = (-self.facing[0],self.facing[1])
            elif self.facing[1] == -1:
              self.facing = self.facing[::-1]
            else:
              pygame.quit()
          
          elif event.key == pygame.K_RIGHT:
            print('right')
            if self.facing[1] == 1: 
              self.facing = self.facing[::-1]
            elif self.facing[1] == -1:
              self.facing = self.facing[::-1]
              self.facing = (-self.facing[0],self.facing[1])
            else:
              pygame.quit()
          elif event.key == pygame.K_DOWN:
            print('down')
            if self.facing[0] == 1: 
              self.facing = self.facing[::-1]
            elif self.facing[0] == -1:
              self.facing = self.facing[::-1]
              self.facing = (self.facing[0],-self.facing[1])
            else:
              pygame.quit()

          elif event.key == pygame.K_UP:
            print('up')
            if self.facing[0] == 1: 
              self.facing = self.facing[::-1]
              self.facing = (self.facing[0],-self.facing[1])
            elif self.facing[0] == -1:
              self.facing = self.facing[::-1]
            else:
              pygame.quit()
          
    self.move_snake()

  ## COLE ADDED (7/31) - INITIAL AGENT
  def agent0(self):
    t_end = time.time() + .1
    while time.time() < t_end:
      if self.facing[0] == 1:
        print('up')
        self.facing = self.facing[::-1]
        #self.facing = (self.facing[0],-self.facing[1])
      else: 
        self.facing = self.facing[::-1]
        self.facing = (self.facing[0],-self.facing[1])

    self.move_snake()

  '''
  def agent1(self):
    move_to_be_chosen = 0
    
    while move_to_be_chosen:
    self.move_snake()
  '''

  ## WILL CONTROL REST OF BODY 
  def move_snake(self):
    '''add new cube(rect) in the direction the snake is facing, and *(IF NO APPLE) chops off the tail'''
    if self.got_apple:
      self.snake_list.insert(0,((self.snake_list[0][0]+int(self.facing[0]))%20,(self.snake_list[0][1]+int(self.facing[1]))%20))
      self.got_apple = False
    else:
      self.snake_list.insert(0,((self.snake_list[0][0]+int(self.facing[0]))%20,(self.snake_list[0][1]+int(self.facing[1]))%20))
      del self.snake_list[-1]

class apple():
  def __init__(self,x_range,y_range,snake_object):
    while True:
      (x,y) = (random.randint(0,x_range)%20,random.randint(0,y_range)%20)
      if (x,y) not in snake_object.snake_list:
        break
    self.position = (x,y)

  def change_apple_position(self,x_range,y_range,snake_object):
    while True:
      (x,y) = (random.randint(0,x_range)%20,random.randint(0,y_range)%20)
      #make sure apple not in snake position
      if (x,y) not in snake_object.snake_list:
        break
    self.position = (x,y)

#added another parameter so snake defaults at a size of 4
def detect_collision(apple_object,snake_object, helper):
  '''detect if snake ran into self/got apple'''
  snake_set = set(snake_object.snake_list) #use set to eliminate duplicate,duplicate means collision
  if (helper < 5):
    snake_object.got_apple = True
  if len(snake_set) != len(snake_object.snake_list):
    '''game over, return score'''
    return len(snake_set)
  if apple_object.position in snake_object.snake_list:
    '''got an apple, keep tail next time snake moves,and generate new apple'''
    snake_object.got_apple = True
    apple_object.change_apple_position(19,19,snake_object)

def draw_grid(w, rows, surface):
  '''draw grid for game window, takes in width, rows, surface(pygame object)'''
  sizeBtwn = w // rows  #e.g. 20x20 would be 1 
  x = 0
  y = 0

  for l in range(rows):
    x = x + sizeBtwn
    y = y + sizeBtwn
    #draws 2 line - surface, dimensions, start pos, end pos
    pygame.draw.line(surface, (255,255,255), (x,0),(x,w)) #ypos wont change
    pygame.draw.line(surface, (255,255,255), (0,y),(w,y)) #xpos wont change

def draw_snake_apple(surface,snake_object,apple_object,dimension,rows):
  '''draw snake and apple on game window'''
  dis = dimension // rows
  #draw apple
  pygame.draw.rect(surface, (255,255,0), (apple_object.position[0]*dis+1,apple_object.position[1]*dis+1, dis-2, dis-2))
  #draw snake
  for tup in snake_object.snake_list:
    pygame.draw.rect(surface, (255,255,255), (tup[0]*dis+1,tup[1]*dis+1, dis-2, dis-2))

def draw_all(surface,snake_object,apple_object,dimension,rows):
  surface.fill((0,0,0))
  draw_snake_apple(surface,snake_object,apple_object,dimension,rows)
  draw_grid(dimension,rows,surface)

def get_env(game_win, fac, snake_list):
  '''return env,facing,reward'''
  #data = list(pygame.image.tostring(self.game_window, 'RGB'))
  #return data,self.s.facing,len(self.s.snake_list)+1
  data = list(pygame.image.tostring(game_win, 'RGB'))
  return data, fac, snake_list

def main():
  GAME_GRID_DIMENSION = 500
  GAME_GRID_ROWS = 20
  #create game window
  game_window = pygame.display.set_mode((GAME_GRID_DIMENSION, GAME_GRID_DIMENSION))
  #create snake and apple
  s = snake(GAME_GRID_ROWS,GAME_GRID_ROWS)
  a = apple(GAME_GRID_ROWS,GAME_GRID_ROWS,s)
  #clock
  clock = pygame.time.Clock()
  while True:
    pygame.time.delay(50)
    clock.tick(10)
    s.apply_action()
    #s.agent1()
    score = detect_collision(a,s)

    #terminate condition
    if score:
      print("Score: " + str(score))
      s = snake(9,9)

    #print(s.snake_list)

    draw_all(game_window,s,a,GAME_GRID_DIMENSION,GAME_GRID_ROWS)
    
    pygame.display.update()

if __name__ == "__main__":
  main()
  