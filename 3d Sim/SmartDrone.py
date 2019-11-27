################### Smart drone Class ################
###Extension of Drone class for intelligent drones ###

from ThreeD import ThreeD
from Drone import Drone
import random
import math
import config as c
import drone_brains


SPEED_LIMIT = c.speed_limit #<----- possibly not required
RANGE = c.firing_range
BULLET_SPEED = c.bullet_speed



#SmartDrone is an extension of the Drone class
class SmartDrone(Drone):
    #Constructor for SmartDrone
    def __init__(self, move_divider, startpos, color, team, behavior):

        #Pass some arguments to the Drone constructor
        Drone.__init__(self, move_divider, startpos)
        self.color = color
        self.real_color = color
        self.team  = team
        self.assignment = None
        self.assigned = False
        self.behavior = getattr(drone_brains, behavior)
        self.behavior_name = behavior
        self.distanceToEnemyCentroid = 0
        if color == 'red':
            self.invincible = c.red_invicible
        else:
            self.invincible = c.blue_invincible


    # Fly to the centroid of neighbors
    def cohesion(self, drones):
        vector = ThreeD(0,0,0)

        #Calculate centroid
        for drone in drones:
            if drone is not self:
                if drone.team == self.team:
                    vector += drone.position
        vector /= (len(drones) +1)

        #return first offset, move 10% of the way to the center
        return (vector - self.position) / 8


    # Make sure that drones don't get too close to each other
    def separation(self, drones):
        vector = ThreeD(0,0,0)
        for drone in drones:
            if drone is not self:
                if drone.team == self.team:
                    if (self.position - drone.position).mag() < 45:
                        vector -= (drone.position - self.position)
        return vector * 1.5


    # ensure that drones are flying at similar velocities
    def alignment(self, drones):
        vector = ThreeD(0,0,0)
        for drone in drones:
            if drone is not self:
                if drone.team == self.team:
                    vector += drone.velocity
        vector /= (len(drones) + 1)
        return (vector - self.velocity) / 8

    '''
    #holding pattern (used to let rabbit drones get in the front)
    def hold_and_wait(self, drones):
        vector = ThreeD(0,0,0)
        for drone in drones:
            vector += drone.position
        if len(drones) > 0:
            vector //= len(drones)

        v1 = self.cohesion(drones)
        v2 = self.separation(drones)
        v3 = self.alignment(drones)
        v4 = (vector - self.position) / 7.5
        self.updatedVelocity = v1 + v2 + v3 + v4
    '''


    #go after the other flock
    def target_enemy(self, drones, enemydrones):
        vector = ThreeD(0,0,0)
        for drone in enemydrones:
            vector += drone.position
        vector /= (len(enemydrones)+1)

        ##### Why divide by 7.5? ######
        return (vector - self.position) / 7.5


    #chase closest target
    def target_select(self, enemydrones):
        vector = ThreeD(0,0,0)
        list1 = []

        #find closest drone using the distance formula
        for drone in enemydrones:
            list1.append(self.distanceToPos(drone.position))
        closest = min(list1)

        #chase enemy based on current position
        for drone in enemydrones:
            if self.distanceToPos(drone.position) == closest:
                vector += drone.position
        return (vector - self.position) / 2


    #Give drones an assigned enemy drone
    def assign(self, drones, enemydrones):
        sorted(drones, key=lambda SmartDrone: SmartDrone.distanceToEnemyCentroid)
        sorted(enemydrones, key=lambda SmartDrone: SmartDrone.distanceToEnemyCentroid)

        for drone in drones:
            for enemy in enemydrones:
                if  enemy.assigned == False:
                    drone.assignment = enemy
                    enemy.assigned = True

        if self.assignment == None:
            self.assignment = enemydrones[0]

        return (self.assignment.position - self.position) / 2


    
    #Fire a bullet if the target is within range
    def fire(self, friendlydrones, enemydrones, RANGE):
        #Equations found on stack overflow 
        bullet_speed = 2000       #need to fix later, make bullet speed configurable
        b_pos = self.position
        fire = False 

        for enemy in enemydrones:
            #If we are out of range of this particular drone then continue to check other drones
            if (self.position - enemy.position).mag() > RANGE:
                continue

            t_pos  = enemy.position
            t_vect = enemy.velocity

            a = (t_vect.x ** 2) + (t_vect.y ** 2) + (t_vect.z ** 2) - (bullet_speed ** 2)
            b = 2 * ((t_pos.x * t_vect.x) + (t_pos.y * t_vect.y) + (t_pos.z * t_vect.z) - (b_pos.x * t_vect.x) + (b_pos.y * t_vect.y) + (b_pos.z * t_vect.z))  
            c = (t_pos.x ** 2) + (t_pos.y ** 2) + (t_pos.z ** 2) + (b_pos.x ** 2) + (b_pos.y ** 2) + (b_pos.z ** 2) - (2 * t_pos.x * b_pos.x) - (2 * t_pos.y * b_pos.y) - (2 * t_pos.z * b_pos.z)

            t1 = (-b + math.sqrt((b**2) - (4 * a * c))) / (2 * a)
            t2 = (-b - math.sqrt((b**2) - (4 * a * c))) / (2 * a)

            t = smallestNotNegorNan(t1,t2)

            #print("T VALUE IS:" + str(t))
            if t == False:
                continue

            t *= self.move_divider
            v = ThreeD(0,0,0)

            v.x = (t_pos.x - b_pos.x + (t * t_vect.mag() * t_vect.x)) / (t * bullet_speed)
            v.y = (t_pos.y - b_pos.y + (t * t_vect.mag() * t_vect.y)) / (t * bullet_speed)
            v.z = (t_pos.z - b_pos.z + (t * t_vect.mag() * t_vect.z)) / (t * bullet_speed)
            v.x = -v.x
            v.y = -v.y
            v.z = -v.z
            multiplyerX = self.velocity.x / v.x
            multiplyerY = self.velocity.y / v.y
            multiplyerZ = self.velocity.z / v.z
            #test_v = v - self.velocity
            #test_v = self.velocity  - v
            #print("Drone color is: " + str(self.real_color))
            #print("Test vector: x = " + str(test_v.x) + " y = " + str(test_v.y) + " z = " + str(test_v.z))
            #print("V vector:    x = " + str(v.x) + " y = " + str(v.y) + " z = " + str(v.z))
            #print("Self vector: x = " + str(self.velocity.x) + " y = " + str(self.velocity.y) + " z = " + str(self.velocity.z))
            if multiplyerY - multiplyerX < .5 and multiplyerY - multiplyerX > -.5:
                if multiplyerZ - multiplyerX < .5 and multiplyerZ - multiplyerX > -.5:
                    fire = True
                    #print("decided to fire")
                    break
            '''
            if test_v.x < 40 and test_v.x > -40:
                if test_v.y < 40 and test_v.y > -40:
                    if test_v.z < 40 and test_v.z > -40:
                        fire = True
                        break

'''
        return fire




#Return the smallest of the two numbers such that they are not negative and are not NaN
def smallestNotNegorNan(t1, t2):
    if math.isnan(t1) and math.isnan(t2):
        return False
    if math.isnan(t1) and t2 < 0:
        return False
    if math.isnan(t2) and t1 < 0:
        return False
    
    x = min(t1, t2)
    y = max(t1, t2)

    if x < 0:
        if y < 0:
            return False
        else:
            return y
    else:
        return x


            

#Check to see if within range
def target_in_range(p1,p2,num):
    if p1 > 0 and p2 > 0:
        if abs(p1 - p2) < num:
            return True
    elif p1 > 0 and p2 < 0:
        if abs(p1 + p2) < num:
            return True
    elif p1 < 0 and p2 > 0:
        if abs(p1 + p2) < num:
            return True
    elif p1 < 0 and p2 < 0:
        if abs(p1 - p2) < num:
            return True
    return False


#check velocities
def vel_target(vx, vy, vz, dx, dy, dz, ex, ey, ez):
    #If pointing up
    if vz > 0:
        #If pointing forward and to right
        if vx > 0 and vy > 0:
            #If enemy is up, forward and to right
            if ex > dx or ey > dy or ez > dz:
                return True
        #If pointing forward and to left
        if  vx < 0 and vy > 0:
            #If enemy is up, forward and to left
            if ex < dx or ey > dy or ez > dz:
                return True
        #If pointing back and to left
        if vx < 0 and vy < 0:
            #If enemy is up, back and to left
            if ex < dx or ey < dy or ez > dz:
                return True
        #If pointing back and to right
        if vx > 0 and vy < 0:
            #If enemy is up, back and to right
            if ex > dx or ey < dy or ez > dz:
                return True
    if vz < 0:
        #If pointing forward and to right
        if vx > 0 and vy > 0:
            #If enemy is up, forward and to right
            if ex > dx or ey > dy or ez < dz:
                return True
        #If pointing forward and to left
        if  vx < 0 and vy > 0:
            #If enemy is up, forward and to left
            if ex < dx or ey > dy or ez < dz:
                return True
        #If pointing back and to left
        if vx < 0 and vy < 0:
            #If enemy is up, back and to left
            if ex < dx or ey < dy or ez < dz:
                return True
        #If pointing back and to right
        if vx > 0 and vy < 0:
            #If enemy is up, back and to right
            if ex > dx or ey < dy or ez < dz:
                return True
    return False


