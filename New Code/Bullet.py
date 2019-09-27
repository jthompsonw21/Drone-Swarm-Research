#Bullet Class
from TwoD import TwoD
import random
import math
import threading

#Max bullet velocity
SPEED_LIMIT = 2000


#Bullet  class, initial position is from the drone that fired the bullet
#Initial velocity is 400m/s
class Bullet:
    #init the location and velocity of the bullet to the drone
    def __init__(self, drone, move_divider):
        self.velocity = drone.velocity * 200
        self.position = self.pos(drone)
        self.move_divider = move_divider * 5
        self.color = "black"
        self.team = drone.real_color

        #make sure that bullets cant fly forever
        self.alive = True
        timer = threading.Timer(3.0, self.death)
        timer.start()

    
    #draw bullet as blackc square
    def draw(self, graph):
        x0 = self.position.x + 1
        y0 = self.position.y + 1
        x1 = self.position.x - 1
        y1 = self.position.y - 1
        graph.create_rectangle((x0,y0,x1,y1), fill = self.color)


    #kills the bullet
    def death(self):
        self.alive = False
    

    #calculate own positino, not starting right on drone
    def pos(self, drone):
        theta = math.atan2(drone.velocity.y, drone.velocity.x)
        x = math.cos(theta) * 5 + drone.position.x
        y = math.sin(theta) * 5 + drone.position.y
        return TwoD(x,y)
    

    #Limit the bullet speed
    def limit_speed(self):
        if self.velocity.mag() > SPEED_LIMIT:
            self.velocity /= self.velocity.mag() / SPEED_LIMIT

    
    #move the bullet
    def move(self):
        self.limit_speed()
        self.position += self.velocity / self.move_divider

