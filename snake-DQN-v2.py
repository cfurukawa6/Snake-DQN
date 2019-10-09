import numpy as np
import random
import math
#from scores.score_logger import ScoreLogger
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

#from snake_game import *
#from snake_OO import *
from my_snake import *


gamma =0.90
learning_rate=0.0007

mem_size = 100
batch_size=32
explore_max = 1
explore_min = 0.000001
#explore_decay=0.999
explore_decay = .99

class DQN:

  def __init__(self,input_dimension, action_space):
    self.exploration_rate = explore_max
    self.action_list = [-1,0,1]
    self.action_space = action_space
    self.memory =deque(maxlen=mem_size)

    #NN stuff
    self.model = Sequential()
    self.model.add(Dense(24, input_shape=(input_dimension,), activation="relu"))
    self.model.add(Dense(24, activation="relu"))
    self.model.add(Dense(24, activation="relu"))
    self.model.add(Dense(self.action_space, activation="linear"))
    self.model.compile(loss="mse", optimizer=Adam(lr=learning_rate))

  def remember(self,state,action,reward,next_state,done):
    self.memory.append((state,action,reward,next_state,done))

  #explore randomly or use NN to get an action
  def get_action(self,state):
    if np.random.rand() < self.exploration_rate:
      #return random.randrange(self.action_list)
      return random.randint(-1,1)
    #print("HERE")
    Q = self.model.predict(state)
    return np.argmax(Q[0])-1

  def experience_replay(self):
    #batch_size = len(self.memory)
    if len(self.memory) < batch_size:
      return
    batch = random.sample(self.memory,batch_size)
    for state,action,reward,state_next,terminal in batch:
      Q_update = reward
      if not terminal:
        Q_update = (reward + gamma *np.amax(self.model.predict(state_next)[0]))
      Q = self.model.predict(state)
      Q[0][action] =Q_update
      self.model.fit(state,Q,verbose=0)
    self.exploration_rate *= explore_decay
    self.exploration_rate =max(explore_min,self.exploration_rate) 

'''
def snake_agent():
  gam = game()
  #solver = DQN(12000)
  prev_reward = 0

  run = 0
  while True:
    run += 1
    while True:
      gam.run_game()
      data,facing,reward = gam.get_env()
      if prev_reward > reward:
        reward = -prev_reward
        x=input()
      print(facing,str(reward))
      prev_reward = reward
      #action = solver.get_action(state)
  #     state_next,reward,terminal,info = env.step(action)
  #     reward = reward if not terminal else -reward
  #     state_next = np.reshape(state_next, [1, observation_space])
  #     solver.remember(state,action,reward,state_next,terminal)
  #     state = state_next
  #     if terminal:
  #       print ("Run: " + str(run) + ", exploration: " + str(solver.exploration_rate) + ", score: " + str(step))
  #       break
  #     solver.experience_replay()
'''
def snake_agent():
  GAME_GRID_DIM = 200
  GAME_GRID_ROW = 20
  moves = ['left', 'right']

  game_window = pygame.display.set_mode((GAME_GRID_DIM, GAME_GRID_DIM))

  s = snake(GAME_GRID_ROW, GAME_GRID_ROW)
  a = apple(GAME_GRID_ROW, GAME_GRID_ROW, s)

  obv_space, facing, reward = get_env(game_window, s.facing, s.snake_list)

  clock = pygame.time.Clock()

  prev_reward = 0

  solver = DQN(len(obv_space), 3)

  run = 0
  while True:
    run +=1 
    helper = 1 #added so the snake will default at a size of 4
    time_constraint = 1

    data1, facing, reward = get_env(game_window, s.facing, s.snake_list)
    data1 = np.reshape(data1, [1,len(obv_space)])
    while True:

      pygame.time.delay(50)
      clock.tick(10)

      #env.run_game()
      #state = data1, facing, reward = env.get_env

      #data1, facing, reward = get_env(game_window, s.facing, s.snake_list)
      #data1 = np.reshape(data1, [1,len(obv_space)])

      action = solver.get_action(data1)
      #print(action, solver.exploration_rate)

      #s.apply_action()
      if action > -1 and action < 2:
        s.apply_action(moves[action])
      else:
        s.apply_action()

      score = detect_collision(a,s, helper)
      helper += 1
      time_constraint *= .99

      state_next, facing, reward = get_env(game_window, s.facing, s.snake_list)
      #reward =  len(reward) if not score else -len(reward)
      '''IDEA: 
          1) If snake doesnt get apple then want to deteriate as time passes
          2) We want snake dying on smaller size worse than dying on larger snake 
      '''
      if helper > 5 and s.got_apple == True:
        reward = len(reward) + 10
      else:
        #reward = len(reward) + (1-time_constraint) if not score else -(400-len(reward)) #400 is max score
        reward = len(reward) + time_constraint if not score else -(400-len(reward)) #400 is max score


      #reward /= 400  #trying to normalize the reward
      #if reward < 0:
        #reward /= 400
        #reward = 400 / reward

      state_next = np.reshape(state_next, [1,len(obv_space)])
      #defaulting snake at 5
      if helper > 5: 
        solver.remember(data1, action, reward, state_next, score) 
      data1 = state_next

      if score:
        f = open("info1.txt", "a")
        f.write("Run: "+ str(run) + ", exploration: " + str(solver.exploration_rate)+ ", score: " +str(score) + "\n")
        f.close

        #print("Score: " + str(score))
        print("Run: ", run, ", exploration: ", solver.exploration_rate, ", score: ", score)
        s = snake(9,9)
        solver.experience_replay()
        break
      #solver.experience_replay()

      draw_all(game_window,s,a, GAME_GRID_DIM, GAME_GRID_ROW)
      pygame.display.update()


if __name__ == "__main__":
  snake_agent()