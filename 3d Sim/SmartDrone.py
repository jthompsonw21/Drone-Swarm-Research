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
        self.distanceToEnemyCentroid = ThreeD(0,0,0)


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
        '''
        #If the drone is a rabbit then don't worry about the separation from friendly drones, 
        # get close to enemy drones but maintain a distance to ensure that attention of enemy is caught
        if self.behavior == 'RABBIT':
            for drone in drones:
                if drone is not self:
                    if  drone.team != self.team:
                        if (self.position - drone.position).mag() < 100:
                            vector -= (drone.position - self.position)

        #If not a rabbit then maintain regular separation from friendly drones
        else:
            for drone in drones:
                if drone is not self:
                    if drone.team == self.team:
                        if (self.position - drone.position).mag() < 45:
                            vector -= (drone.position - self.position)
        '''
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
    #What is the difference between  this an above target selection? 
    def ASSIGN_NEAREST(self, drones, enemydrones):
        #print "Currently using behavior mode ASSIGN_NEAREST"
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
                






            

























