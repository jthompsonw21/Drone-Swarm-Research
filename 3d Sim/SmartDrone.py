################### Smart drone Class ################
###Extension of Drone class for intelligent drones ###

from ThreeD import ThreeD
from Drone import Drone
import random
import math
import config as c


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
        self.behavior = getattr(SmartDrone, behavior)
        self.behavior_name = behavior
        self.distanceToEnemyCentroid = ThreeD(0,0,0)
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


    ############################################
    ########## Drone Behavior Methods ##########
    ############################################




    # Set drone activity mode to RABBIT
    def RABBIT(self,drones, enemydrones):
        #Put in arbitrary destination points for the rabbits until we can find a better solution
        if self.real_color == 'red':
            DEST = ThreeD(900,300,500)
        elif self.real_color == 'blue':
            DEST = ThreeD(300,900,500)

        #find the centroid of the enemy drones
        self.distanceToEnemyCentroid = self.calculateDistanceToSwarm(enemydrones)
        #find the closest enemydrone
        close = ThreeD(0,0,0)
        list1 = []

        for drone in enemydrones:
            list1.append(self.distanceToPos(drone.position))
        if(len(list1) != 0):
            closest = min(list1)

        #chase enemy based on current position
        for drone in enemydrones:
            if self.distanceToPos(drone.position) == closest:
                close += drone.position

        # Now determine if we want to runaway or not
        RUNAWAY = False
        if self.position.y > close.y-(RANGE):
            if self.position.y < close.y+(RANGE):
                if self.position.x > close.x-(RANGE):
                    if self.position.x < close.x+(RANGE):
                        if self.position.z > close.z-(RANGE):
                            if self.position.z < close.z+(RANGE):
                                RUNAWAY = True

        if RUNAWAY == False:
            v1 = (close - self.position) / 2
        else:
            r = random.randint(0,1)
            if r == 0:
                self.color = "white"
            else:
                self.color = self.real_color

            v1 = DEST - self.position
        self.updatedVelocity = v1



    #Set drone activity to flocking
    def FLOCKING(self, drones, enemydrones):
        #print "In flocking behavior mode"
        self.distanceToEnemyCentroid = self.calculateDistanceToSwarm(enemydrones)
        if len(drones) > 1:
            #Use our flocking rules to get an updated velocity
            v1 = self.cohesion(drones)
            v2 = self.separation(drones)
            v3 = self.alignment(drones)
            v4 = self.target_enemy(drones, enemydrones)
            self.updatedVelocity = v1 + v2 + v3 + v4
        else:
            v4 = self.target_enemy(drones, enemydrones)
            self.updatedVelocity = v4



    ##############################################
    ########## Target Selection Methods ##########
    ##############################################

    #Selects the nearest enemy drone as the primary target
    def SELECT_NEAREST(self, drones, enemydrones):
        self.distanceToEnemyCentroid = self.calculateDistanceToSwarm(enemydrones)
        attack = False
        for drone in enemydrones:
            if self.position.y > drone.position.y - RANGE:
                if self.position.y < drone.position.y + RANGE:
                    if self.position.x > drone.position.x - RANGE:
                        if self.position.x < drone.position.x + RANGE:
                            if self.position.z > drone.position.z - (RANGE):
                                if self.position.z < drone.position.z + (RANGE):
                                    attack = True

            #do target select
            if(attack):
                r = random.randint(0,1)
                if r == 0:
                    self.color = "white"
                else:
                    self.color = self.real_color
                v1 = self.target_select(enemydrones)
                self.updatedVelocity = v1

            #otherwise act normally
            else:
                self.FLOCKING(drones, enemydrones)


    #Uses assignment to tell the drones which to shoot at (still need some clarification)
    def ASSIGN_NEAREST(self, drones, enemydrones):
        #NEED TO FIX HOLD AND WAIT ROUTINE
        '''
        # check to see if there are any rabbits. If there are,
        # then check distance to centroid of rabbits. If centroid is too close,
        # hold and wait. Otherwise proceed to try to attack
        holdWait = False
        rabbit_list = []
        for drone in drones:
            if drone.behavior_name == 'RABBIT':
                rabbit_list.append(drone)
        #compute rabbit centroid
        if len(rabbit_list) > 0:
            rabbit_centroid = ThreeD(0,0,0)
            for rabbit in rabbit_list:
                rabbit_centroid += rabbit.position
            rabbit_centroid //= (len(rabbit_list))
            dist_rabbit_centroid = self.distanceToPos(rabbit_centroid)
            if dist_rabbit_centroid < 100:
                holdWait = True
                self.hold_and_wait(drones)

        if holdWait == False:
            attack = False
            self.distanceToEnemyCentroid = self.calculateDistanceToSwarm(enemydrones)

            #Determine if we need to attack
            for drone in enemydrones:
                if self.position.y > drone.position.y - RANGE:
                    if self.position.y < drone.position.y + RANGE:
                        if self.position.x > drone.position.x - RANGE:
                            if self.position.x < drone.position.x + RANGE:
                                if self.position.z > drone.position.z - (RANGE):
                                    if self.position.z < drone.position.z + (RANGE):
                                        attack = True
            #If we need to attack
            if(attack):
                r = random.randint(0, 1)
                if r == 0:
                    self.color = "white"
                else:
                    self.color = self.real_color
                    print('Hold and wait value:' + str(holdWait))
                    v1 = self.assign(drones, enemydrones)
                    self.updatedVelocity = v1

            #If we don't attack then just flock
            else:
                #print "We need to flock"
                self.FLOCKING(drones, enemydrones)

            for enemy in enemydrones:
                enemy.assigned = False
            for drone in drones:
                drone.assignment = None
        '''
        attack = False
        self.distanceToEnemyCentroid = self.calculateDistanceToSwarm(enemydrones)

        #Determine if we need to attack
        for drone in enemydrones:
            if self.position.y > drone.position.y - RANGE:
                if self.position.y < drone.position.y + RANGE:
                    if self.position.x > drone.position.x - RANGE:
                        if self.position.x < drone.position.x + RANGE:
                            if self.position.z > drone.position.z - (RANGE):
                                if self.position.z < drone.position.z + (RANGE):
                                    attack = True
        #If we need to attack
        if(attack):
            r = random.randint(0, 1)
            if r == 0:
                self.color = "white"
            else:
                self.color = self.real_color
                #print('Hold and wait value:' + str(holdWait))
                v1 = self.assign(drones, enemydrones)
                self.updatedVelocity = v1

        #If we don't attack then just flock
        else:
            #print "We need to flock"
            self.FLOCKING(drones, enemydrones)

        for enemy in enemydrones:
            enemy.assigned = False
        for drone in drones:
            drone.assignment = None


    
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

            if t == False:
                continue
            
            v = ThreeD(0,0,0)

            v.x = (t_pos.x - b_pos.x + (t * t_vect.mag() * t_vect.x)) / (t * bullet_speed)
            v.y = (t_pos.y - b_pos.y + (t * t_vect.mag() * t_vect.y)) / (t * bullet_speed)
            v.z = (t_pos.z - b_pos.z + (t * t_vect.mag() * t_vect.z)) / (t * bullet_speed)

            test_v = v - self.velocity
            print("Test vector: x = " + str(test_v.x) + " y = " + str(test_v.y) + " z = " + str(test_v.z))
            print("Self vector: x = " + str(self.velocity.x) + " y = " + str(self.velocity.y) + " z = " + str(self.velocity.z))
            if test_v.x < 5 and test_v.x > -5:
                if test_v.y < 5 and test_v.y > -5:
                    if test_v.z < 5 and test_v.z > -5:
                        fire = True
                        break

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


