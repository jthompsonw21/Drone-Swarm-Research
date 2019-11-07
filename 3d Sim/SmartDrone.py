################### Smart drone Class ################
###Extension of Drone class for intelligent drones ###

from ThreeD import ThreeD
from Drone import Drone
import random
import math
import config as c


SPEED_LIMIT = c.speed_limit #<----- possibly not required
RANGE = c.firing_range



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
    #def RABBIT(self,drones, enemydrones, DEST):
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
            v1 = self.cohesion(drones)
            v2 = self.separation(drones)
            v3 = self.alignment(drones)
            v4 = self.target_enemy(drones, enemydrones)
            #print "v1 = " + str(v1) + "  v2 = " + str(v2) + "  v3 = " + str(v3) + "  v4 = " + str(v4)
            self.updatedVelocity = v1 + v2 + v3 + v4
        else:
            v4 = self.target_enemy(drones, enemydrones)
            self.updatedVelocity = v4



    ##############################################
    ########## Target Selection Methods ##########
    ##############################################

    #Type of target selection #####find out later####
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


    #Other type of target selection
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
        #Calculate the drone's xy angle and pitch
        theta = math.atan2(self.velocity.y,  self.velocity.x)
        phi = math.atan2(self.xyVelocityMag(), self.velocity.z)

        x1 = self.position.x
        y1 = self.position.y
        z1 = self.position.z
        x2 = math.cos(theta)* 300 + x1
        y2 = math.sin(theta)* 300 + y1
        z2 = math.sin(phi)*   300 + z1

        dxdy = (y2-y1)/(x2-x1)
        dvdz = dxdy/(z2-z1+1)
        def f(x):
            return y1+dxdy*(x-x1)
        def g(x):
            return z1+dvdz*(z2-z1)
        def test1(x,y,tol):
            return abs(y-f(x)) <= tol
        def test2(x,y,tol):
            return abs(y-g(x)) <= tol

        Fire = False
        Safe = True

        for enemy in enemydrones:
            if test1(enemy.position.x, enemy.position.y, 300):
                positionMag = math.sqrt((enemy.position.x **2)+(enemy.position.y **2))
                if test2(positionMag, enemy.position.z, 300):
                    if target_in_range(enemy.position.x, self.position.x, RANGE):
                        if target_in_range(enemy.position.y, self.position.y, RANGE):
                            if target_in_range(enemy.position.z, self.position.z, RANGE):
                                if vel_target(self.velocity.x, self.velocity.y, self.velocity.z, self.position.x, self.position.y, self.position.z, enemy.position.x, enemy.position.y, enemy.position.z):
                                    Fire = True

            for friendly in friendlydrones:
                if test1(friendly.position.x, enemy.position.y, 10):
                    Safe = False

        if Fire == True and Safe == True:
            return True

        return False

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


