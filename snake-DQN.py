import gym
import numpy as np
import random
import math
#from scores.score_logger import ScoreLogger
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

from my_snake import *

env_name = 'CartPole-v0'

gamma =0.90
learning_rate=0.0007

mem_size =100000
batch_size=32
explore_max = 1
explore_min = 0.000001
explore_decay=0.999

class DQN:

  def __init__(self,observation_space,action_space):
    self.exploration_rate = explore_max
    self.action_space =action_space
    self.memory =deque(maxlen=mem_size)

    #NN stuff
    self.model = Sequential()
    self.model.add(Dense(24, input_shape=(observation_space,), activation="relu"))
    self.model.add(Dense(24, activation="relu"))
    self.model.add(Dense(24, activation="relu"))
    self.model.add(Dense(self.action_space, activation="linear"))
    self.model.compile(loss="mse", optimizer=Adam(lr=learning_rate))

  def remember(self,state,action,reward,next_state,done):
    self.memory.append((state,action,reward,next_state,done))

  #explore randomly or use NN to get an action
  def get_action(self,state):
    if np.random.rand() < self.exploration_rate:
      return random.randrange(self.action_space)
    Q = self.model.predict(state)
    print(np.argmax(Q[0]))
    return np.argmax(Q[0])
  
  def experience_replay(self):
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


def cartpole():
  env = gym.make(env_name)
  #score_logger = ScoreLogger(env_name)
  env._max_episode_steps= 200
  observation_space =env.observation_space.shape[0]
  action_space = env.action_space.n

  #print('obv: ', observation_space)
  #print('act: ', action_space)

  solver = DQN(observation_space,action_space)
  run = 0
  while True:
    run += 1
    state = env.reset()
    state = np.reshape(state,[1,observation_space])
    step = 0 
    while True:
      step += 1
      env.render()
      action = solver.get_action(state)
      state_next,reward,terminal,info = env.step(action)
      reward = reward if not terminal else -reward
      state_next = np.reshape(state_next, [1, observation_space])
      solver.remember(state,action,reward,state_next,terminal)
      state = state_next
      if terminal:
        print ("Run: " + str(run) + ", exploration: " + str(solver.exploration_rate) + ", score: " + str(step))
        break
      solver.experience_replay()


def main_snake():
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
  
  cartpole()
  #main_snake()