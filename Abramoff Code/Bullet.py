# BULLET IMPLEMENTATION CLASS
from TwoD import TwoD

import random 
import math
import threading

SPEED_LIMIT = 2000       # FOR BULLET VELOCITY

#Bullet class, initial position from drone, velocity is 400m/s
class Bullet:

  #initialize the bullet to the location and velocity of the drone
    def __init__(self, drone, move_divider):
        self.velocity = drone.velocity * 200
        self.position = self.pos(drone)
        self.move_divider = move_divider * 5
        self.color = "black"
        self.team = drone.real_color
        #make sure bullet cant fly forever
        self.alive = True
        timer = threading.Timer(3.0, self.death)
        timer.start()

    #draw bullet as black square
    def draw(self, graph):
      x0 = self.position.x + 1
      y0 = self.position.y + 1
      x1 = self.position.x - 1
      y1 = self.position.y - 1
      graph.create_rectangle((x0, y0, x1, y1), fill = self.color)


    #kill bullet
    def death(self):
      self.alive = False

    #calculate own position, not starting right on drone
    def pos(self, drone):
      theta = math.atan2(drone.velocity.y, drone.velocity.x)
      x = math.cos(theta) * 5 + drone.position.x
      y = math.sin(theta) * 5 + drone.position.y
      return TwoD(x,y)

    # Limit drone speed.    
    def limit_speed(self):
      if self.velocity.mag() > SPEED_LIMIT:
        self.velocity /= self.velocity.mag() / SPEED_LIMIT

    #move the bullet
    def move(self):
       self.limit_speed()
       self.position += self.velocity / self.move_divider
