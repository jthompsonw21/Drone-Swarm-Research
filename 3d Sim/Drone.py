###Drone Parent Class##


from ThreeD import ThreeD
import random
import math
import numpy as np
import config as c
import copy
import quaternion as quat

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

        #Using quaternion theory we minimize the difference in angle between the old velocity and the updated veclocity vectors
        if self.past_velocity.mag() != 0 and self.velocity.mag() != 0:
            try:
                clockwise = None
                dot = self.velocity.dot(self.past_velocity)
                theta = math.acos(dot / (self.velocity.mag() * self.past_velocity.mag()))
                threshold = np.deg2rad(80/60)
                #print("Initial Theta: " + str(theta))
                #print("Threshold: " + str(threshold))

                #If the angle between the new and old velocities is greater than the threshold, then minimize
                if theta > threshold:
                    #print("Reduction required...")
                    new_theta = theta - threshold
                    v = np.array([0.] + list(self.velocity))
                    rot_axis = np.array([0.] + list(self.velocity.cross(self.past_velocity)))
                    axis_angle = (new_theta * .5) * rot_axis/np.linalg.norm(rot_axis)

                    #Create the quaternions qvec and qlog using the library and get the unit rotation q by thaking the exponential
                    qvec = quat.quaternion(*v)
                    qlog = quat.quaternion(*axis_angle)
                    q = np.exp(qlog)

                    v_prime = q * qvec * quat.quaternion(q.real, *(-q.imag))

                    final = v_prime.imag
                    self.velocity = ThreeD(final[0], final[1], final[2])

                    dot = self.velocity.dot(self.past_velocity)
                    final_theta = math.acos(dot/ (self.velocity.mag() * self.past_velocity.mag()))
                    #print("Resulting theta after math: " + str(final_theta))
            except:
                pass


	    #Now make sure that we restrict max upward and downward angles
        if self.past_velocity.mag()  != 0 and self.velocity.mag() != 0:
            try:
                up = None
                theta = math.atan2(self.velocity.z, self.velocity.xymag())

		#No more than 70 degrees above or below the horizontal
                threshold = np.deg2rad(70)

                if theta > threshold or theta < -(threshold):
                    new_theta = -(theta - threshold)
                    oldxy = self.velocity.xymag()
                    oldz  = self.velocity.z
                    fakexy = 0
                    fakexy = oldxy * math.cos(new_theta) - oldz * math.sin(new_theta)

                    multiplier = fakexy/oldxy
                    self.velocity.x *= multiplier
                    self.velocity.y *= multiplier
                    self.velocity.z = oldxy * math.sin(new_theta) + oldz * math.cos(new_theta)
            except:
                pass


    # Calculate the distance from this drone to the centroid of another drone swarm
    def calculateDistanceToSwarm(self, drones):
        centerDrones = ThreeD(0,0,0)
        for drone in drones:
            centerDrones += drone.position
        if len(drones) > 0:
            centerDrones //= (len(drones))
        return self.distanceToPos(centerDrones)




