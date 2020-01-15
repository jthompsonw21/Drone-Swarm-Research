from ThreeD import ThreeD
from Drone import Drone
import config as c 
import random

RANGE = c.firing_range
CEILING = c.ceiling
HEIGHT = c.height
WIDTH = c.width



############################################
########## Drone Behavior Methods ##########
############################################
# Set drone activity mode to RABBIT
def RABBIT(drone,drones, enemydrones):
    #Put in arbitrary destination points for the rabbits until we can find a better solution
    if drone.real_color == 'red':
        DEST = ThreeD(900,300,500)
    elif drone.real_color == 'blue':
        DEST = ThreeD(300,900,500)

    #find the centroid of the enemy drones
    drone.distanceToEnemyCentroid = drone.calculateDistanceToSwarm(enemydrones)
    #find the closest enemydrone
    close = ThreeD(0,0,0)
    list1 = []

    for enemy in enemydrones:
        list1.append(drone.distanceToPos(enemy.position))
    if(len(list1) != 0):
        closest = min(list1)

    #chase enemy based on current position
    for enemy in enemydrones:
        if drone.distanceToPos(enemy.position) == closest:
            close += enemy.position

    # Now determine if we want to runaway or not
    RUNAWAY = False
    if drone.position.y > close.y-(RANGE):
        if drone.position.y < close.y+(RANGE):
            if drone.position.x > close.x-(RANGE):
                if drone.position.x < close.x+(RANGE):
                    if drone.position.z > close.z-(RANGE):
                        if drone.position.z < close.z+(RANGE):
                            RUNAWAY = True

    if RUNAWAY == False:
        v1 = (close - drone.position) / 2
    else:
        r = random.randint(0,1)
        if r == 0:
            drone.color = "white"
        else:
            drone.color = drone.real_color

        v1 = DEST - drone.position
    drone.updatedVelocity = v1



#Set drone activity to flocking
def FLOCKING(drone, drones, enemydrones):
    #print "In flocking behavior mode"
    drone.distanceToEnemyCentroid = drone.calculateDistanceToSwarm(enemydrones)
    if len(drones) > 1:
        #Use our flocking rules to get an updated velocity
        v1 = drone.cohesion(drones)
        v2 = drone.separation(drones)
        v3 = drone.alignment(drones)
        v4 = drone.target_enemy(drones, enemydrones)
        drone.updatedVelocity = v1 + v2 + v3 + v4
    else:
        v4 = drone.target_enemy(drones, enemydrones)
        drone.updatedVelocity = v4



##############################################
########## Target Selection Methods ##########
##############################################

#Selects the nearest enemy drone as the primary target
def SELECT_NEAREST(drone, drones, enemydrones):
    drone.distanceToEnemyCentroid = drone.calculateDistanceToSwarm(enemydrones)
    attack = False
    for enemy in enemydrones:
        if drone.position.y > enemy.position.y - RANGE:
            if drone.position.y < enemy.position.y + RANGE:
                if drone.position.x > enemy.position.x - RANGE:
                    if drone.position.x < enemy.position.x + RANGE:
                        if drone.position.z > enemy.position.z - (RANGE):
                            if drone.position.z < enemy.position.z + (RANGE):
                                attack = True

        #do target select
        if(attack):
            r = random.randint(0,1)
            if r == 0:
                drone.color = "white"
            else:
                drone.color = drone.real_color
            v1 = drone.target_select(enemydrones)
            drone.updatedVelocity = v1

        #otherwise act normally
        else:
            FLOCKING(drone, drones, enemydrones)


#Uses assignment to tell the drones which to shoot at (still need some clarification)
def ASSIGN_NEAREST(drone, drones, enemydrones):
    attack = False
    drone.distanceToEnemyCentroid = drone.calculateDistanceToSwarm(enemydrones)

    #Determine if we need to attack
    for enemy in enemydrones:
        if drone.position.y > enemy.position.y - RANGE:
            if drone.position.y < enemy.position.y + RANGE:
                if drone.position.x > enemy.position.x - RANGE:
                    if drone.position.x < enemy.position.x + RANGE:
                        if drone.position.z > enemy.position.z - (RANGE):
                            if drone.position.z < enemy.position.z + (RANGE):
                                if drone.distanceToPos(enemy.position) < 100:
                                    drone.slowDown = True
                                    #print("Distance from drone "+ str(drone.distanceToPos(enemy.position)))
                                else:
                                    drone.slowDown = False
                                attack = True
    #If we need to attack
    if(attack):
        r = random.randint(0, 1)
        if r == 0:
            drone.color = "white"
        else:
            drone.color = drone.real_color
            v1 = drone.assign(drones, enemydrones)
            drone.updatedVelocity = v1

    #If we don't attack then just flock
    else:
        FLOCKING(drone, drones, enemydrones)

    for enemy in enemydrones:
        enemy.assigned = False
    for d in drones:
        d.assignment = None

def HOLD_AND_WAIT(drone, drones, enemydrones):
    centerDrones = drone.calculateDistanceToSwarm(drones)
    if len(drones) > 1:
        v1 = drone.cohesion(drones)
        v2 = drone.separation(drones)
        v3 = drone.alignment(drones)
        #Targets own swarm 
        #Essentially makes the swarm fly toward itself
        v4 = drone.target_enemy(drones, drones)
        drone.updatedVelocity = v1 + v2 + v3 + v4
    else:
        v4 = drone.target_enemy(drones, drones)
        drone.updatedVelocity = v4


def SPLIT_FORMATION(drone, drones, enemydrones):
    #Similar to rabbit but maintains a distance from the enemy swarm. 
    #Also maintains a certain (larger) distance from friendly drones
    drone.distanceToEnemyCentroid = drone.calculateDistanceToSwarm(enemydrones)
    minDistance = drone.distanceToEnemyCentroid
    selectedDrone = enemydrones[0]
    for enemy in enemydrones: 
        if (drone.position - enemy.position).mag() < (drone.position - selectedDrone.position).mag():
            selectedDrone = enemy
    v1 = maintainDistance(drone, selectedDrone, RANGE)
    drone.updatedVelocity = v1
            

#Generate an update velocity to maintain a certain distance from the enemy drone
def maintainDistance(drone, enemydrone, distance):
    vector = ThreeD(0,0,0)
    if (drone.position - enemydrone.position).mag() < distance:
        vector -= (enemydrone.position - drone.position)
    vector += ThreeD(WIDTH/10, HEIGHT/10, CEILING/20)
    #Maybe increase return value multiplier
    return vector * 1.5


#Runaway from the enemy drone swarm. This is essentially just flocking but in the opposite direction
def RUNAWAY(drone, drones, enemydrones):
    drone.distanceToEnemyCentroid = drone.calculateDistanceToSwarm(enemydrones)
    if len(drones) > 1:
        v1 = drone.cohesion(drones)
        v2 = drone.separation(drones)
        v3 = drone.alignment(drones)
        v4 = drone.target_enemy(drones, enemydrones)
        v4 = v4 * -1
        drone.updatedVelocity = v1 + v2 + v3 + v4
    else:
        v4 = drone.target_enemy(drones, enemydrones)
        v4 = v4 * -1
        drone.updatedVelocity = v4








