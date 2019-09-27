###Drone Parent Class##


from TwoD import TwoD
import random
import math
import config as c

SPEED_LIMIT = c.speed_limit                                          # FOR DRONE VELOCITY
RANGE = c.firing_range                                               # DRONE FIRING RANGE

class Drone:

    #initial drone, position, velocity
    def __init__(self, move_divider, startpos):

        #Initialize the velocity to 0
        self.velocity = TwoD(0,0)                     
        self.updatedVelocity = TwoD(0,0)
        r1 = random.randint(1,100)
        r2 = random.randint(1,100)

        #Randomize the starting position
        self.position = TwoD(startpos-r1, startpos-r2) 
        self.move_divider = move_divider * 5
    
    # Random initial starting values
    def random_start(self, width, height, offset):                   
        if random.randint(0, 1):
            y = random.randint(1, height)
            if random.randint(1,1):
                x = -offset
            else:
                x = width + offset
        else:
            x = random.randint(1, width)
            if random.randint(0, 1):
                y = -offset
            else:
                y = height + offset
        return x, y


    # DRAWS THE DRONE AS A CIRCLE WITH A LINE
    def draw(self, graph):       
        theta = math.atan2(self.velocity.y, self.velocity.x)
        centerx = self.position.x
        centery = self.position.y
        x1 = self.position.x + 3
        y1 = self.position.y + 3
        x2 = self.position.x - 3
        y2 = self.position.y - 3

        linex = math.cos(theta) * 7 + centerx
        liney = math.sin(theta) * 7 + centery

        graph.create_oval(x1,y1,x2,y2, fil = self.color)
        graph.create_line(centerx, centery, linex, liney, fill = 'black')


    # MOVES THE DRONE BASED ON NEW VELOCITIES
    def move(self):
        self.velocity += self.updatedVelocity
        self.limit_speed()
        self.position += self.velocity / self.move_divider


    # SIMPLY CALCULATE THE DISTANCE FROM DRONE TO A POSITION
    def distanceToPos(self,  Pos):                                           
        x = (self.position.x - Pos.x)**2
        y = (self.position.y - Pos.y)**2
        return math.sqrt(x + y)
    

    # Limit the drone's speed
    def  limit_speed(self):
        if self.velocity.mag() > SPEED_LIMIT:
            self.velocity /= self.velocity.mag() / SPEED_LIMIT


    # Calculate the distance from this drone to the centroid of another drone swarm
    def calculateDistanceToSwarm(self, drones):
        centerDrones = TwoD(0,0)
        for drone in drones:
            centerDrones += drone.position
        if len(drones) > 0:
            centerDrones /= (len(drones))
        return self.distanceToPos(centerDrones)










