###Drone Parent Class##


from ThreeD import ThreeD
import random
import math
import numpy as np
import config as c
import copy 

SPEED_LIMIT = c.speed_limit                                          # FOR DRONE VELOCITY
SPEED_MIN   = c.speed_min
RANGE = c.firing_range                                               # DRONE FIRING RANGE
AMULT = c.ascentMultiplier
DMULT = c.descentMultiplier
OUTLINE = c.DRONE_OUTLINE

class Drone:

    #initial drone, position, velocity
    def __init__(self, move_divider, startpos):

        #Initialize the velocity to 0
        self.velocity = ThreeD(0,0,0)
        self.past_velocity = ThreeD(0,0,0)
        self.updatedVelocity = ThreeD(0,0,0)
        self.slowDown = False
        r1 = random.randint(1,100)
        r2 = random.randint(1,100)
        r3 = random.randint(1,100)

        #Randomize the starting position
        self.position = ThreeD(startpos-r1, startpos-r2, startpos-r3)
        self.move_divider = move_divider * 5


    # DRAWS THE DRONE AS A CIRCLE WITH A LINE
    def draw(self, graph):
        #Where drone is facing 
        theta = math.atan2(self.velocity.y, self.velocity.x)
        centerx = self.position.x
        centery = self.position.y
        x1 = self.position.x + 3
        y1 = self.position.y + 3
        x2 = self.position.x - 3
        y2 = self.position.y - 3

        scaleFactor = self.position.z/10

        linex = math.cos(theta) * 7 + centerx
        liney = math.sin(theta) * 7 + centery

        #We can also choose to draw an outline around the drone which changes in size depending on the drone's altitude
        if OUTLINE:
            graph.create_oval(x1+scaleFactor, y1+scaleFactor, x2-scaleFactor, y2-scaleFactor, outline='#000')
        graph.create_oval(x1,y1,x2,y2, fil = self.color)
        graph.create_line(centerx, centery, linex, liney, fill = 'black')


    # MOVES THE DRONE BASED ON NEW VELOCITIES
    def move(self):
        if(self.velocity.z > 0):
            self.updatedVelocity.z *= AMULT
        elif(self.velocity.z < 0):
            self.updatedVelocity.z *= DMULT
        self.past_velocity = copy.deepcopy(self.velocity)
        self.velocity += self.updatedVelocity
        self.limit_speed()
        self.position += self.velocity / self.move_divider


    # SIMPLY CALCULATE THE DISTANCE FROM DRONE TO A POSITION
    def distanceToPos(self,  Pos):
        x = (self.position.x - Pos.x)**2
        y = (self.position.y - Pos.y)**2
        z = (self.position.z - Pos.z)**2
        return math.sqrt(x + y + z)


    # Limit the drone's speed
    def  limit_speed(self):
        
        #Turn radius in the x y plane 
        #print('New (beginning):' + str(self.velocity))
        ##print('Old: ' + str(self.past_velocity))
        #print("Updated" + str(self.updatedVelocity))
                #phi = math.atan2(dv.z, dv.xymag())
        #If the turn rate is greater than 10 degrees (per timestep (1/60th sec)) then lessen the turn rate
        if self.past_velocity.xymag() != 0 and self.velocity.xymag() != 0:
            clockwise = None
            try:
                dot = (self.velocity.x * self.past_velocity.x) + (self.velocity.y * self.past_velocity.y)
                theta = math.acos(dot / (self.velocity.xymag() * self.past_velocity.xymag()))

                threshold = np.deg2rad(15/60)

                #figure out if rotated counterclockwise or clockwise 
                if self.past_velocity.y*self.velocity.x > self.past_velocity.x*self.velocity.y:
                    #print('counterclockwise')
                    clockwise = True
                else: 
                    #print('clockwise')
                    clockwise = False

                #print('Theta: ' + str(theta))
                #print("Threshold: " + str(threshold))
                if theta > (threshold):
                    #print("Limiting turn rate")
                    oldy = self.velocity.y
                    oldx = self.velocity.x
                    oldz = self.velocity.z
                    if clockwise == False:
                        newtheta = -1 * (theta - threshold)
                        ##print('New Theta (from subtraction: counterclockwise): ' + str(newtheta))
                        self.velocity.x = oldx * math.cos(newtheta) - oldy * math.sin(newtheta)
                        self.velocity.y = oldx * math.sin(newtheta) + oldy * math.cos(newtheta)
                        ##print("x: " + str(self.velocity.x) + " y: " + str(self.velocity.y))
                    else:
                        newtheta = -1 * (theta + threshold)
                        ##print('New Theta (from subtraction: clockwise): ' + str(newtheta))
                        self.velocity.x = oldx * math.cos(newtheta) - oldy * math.sin(newtheta)
                        self.velocity.y = oldx * math.sin(newtheta) + oldy * math.cos(newtheta)
                        ##print("x: " + str(self.velocity.x) + " y: " + str(self.velocity.y))

                dot = (self.velocity.x * self.past_velocity.x) + (self.velocity.y * self.past_velocity.y)
                theta = math.acos(dot / (self.velocity.xymag() * self.past_velocity.xymag()))
                #print('New Theta (from vector): ' + str(theta))
            except:
                pass
            
        if self.velocity.mag() > SPEED_LIMIT:
            self.velocity /= self.velocity.mag() / SPEED_LIMIT
        if self.slowDown:
            self.velocity *= .8
        if self.velocity.mag() < SPEED_MIN:
            if self.velocity.mag() == 0:
                r = random.randint(0,100)
                s = random.randint(0,100)
                self.velocity = ThreeD(r,s,0)
            else:
                mult = SPEED_MIN / self.velocity.mag()
                self.velocity *= mult
        
        #print('New (end):' + str(self.velocity))

        #If the climb/dive rate is greater than 45 degrees then lessen the rate
        #if phi > (math.radians(100/math.pi)) or phi < -(math.radians(100/math.pi)):
            #self.velocity.z = self.xyVelocityMag() * math.tan(math.radians(100/math.pi))
        '''
        dot = (self.velocity.x * self.past_velocity.x) + (self.velocity.y * self.past_velocity.y)
        theta = math.acos(dot / (self.velocity.xymag() * self.past_velocity.xymag() + .001))
        print("Resulting theta: " + str(theta))
        print('')
        '''



    # Calculate the distance from this drone to the centroid of another drone swarm
    def calculateDistanceToSwarm(self, drones):
        centerDrones = ThreeD(0,0,0)
        for drone in drones:
            centerDrones += drone.position
        if len(drones) > 0:
            centerDrones //= (len(drones))
        return self.distanceToPos(centerDrones)

    # Calculate the magnitude of the x and y velocity components
    def xyVelocityMag(self):
        return math.sqrt((self.velocity.x **2) + (self.velocity.y **2))












