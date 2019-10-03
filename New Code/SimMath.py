#import some standard python libraries
import random
import math
import  timeit
import config as c
import sys

#import the classes that we need for visuals
from Drone import Drone
from SmartDrone import SmartDrone
from Bullet import Bullet
from TwoD import TwoD

FIRE = c.battle_on
RED_DRONES_AMT  = c.red_drones
BLUE_DRONES_AMT = c.blue_drones
RANGE = c.firing_range
BLUE_BEHAVIOR = c.blue_drone_behavior
RED_BEHAVIOR  = c.red_drone_behavior
WIDTH = c.height
HEIGHT = c.width
WALL = c.wall
WALL_FORCE = c.wall_force
DRONE_RADIUS = 3
OFFSET_START = 20
FRAMES_PER_SEC = c.frames_per_sec
SIMSPEED = c.simspeed
TURN_AROUND = c.avoidance_speed


#Moves the drones and bullets
def move(red_drones, blue_drones, bullet_list):
    print "Moving red drones"
    #Start with the red drones
    for drone in red_drones:
        print "Before move position: " + str(drone.position) + "  Velocity: " + str(drone.velocity)
        simulate_wall(drone)
        detect_enemy(drone, blue_drones)
        drone.behavior(drone, red_drones, blue_drones)
        #Check to see if drones can fire at each other. If so, then fire
        if FIRE:
            fire(drone, red_drones, blue_drones)
        drone.move()

        #Check to see if the current drone is out of bounds
        outofbounds(drone,red_drones)
        print "After move position: " + str(drone.position) + "  Velocity: " + str(drone.velocity)

        #Check to see if the current drone is killed or collided with an enemy drone
        if(killed(drone, bullet_list) or collision(drone, blue_drones)):
            red_drones.remove(drone)
            print "Number of red drones left: "
            print len(red_drones)


    #Redo same thing with blue drones
    for drone in blue_drones:
        simulate_wall(drone)
        detect_enemy(drone, red_drones)
        drone.behavior(drone, blue_drones, red_drones)
        if FIRE:
            fire(drone, blue_drones, red_drones)
        drone.move()
        outofbounds(drone, blue_drones)
        if(killed(drone, bullet_list) or  collision(drone, red_drones)):
            blue_drones.remove(drone)
            print("Number of blue drones left:")
            print len(blue_drones)


    #Move bullets or remove 
    for bullet in bullet_list:
        if bullet.alive:
            bullet.move()
        else:
            bullet_list.remove(bullet)


#Fire a  bullet if the target is within range. Friendly Fire? 
def fire(drone, friendlydrones, enemydrones):
    #If no enemies left then return
    if len(enemydrones) == 0:
        return 

    #Calc drone's current position and orientation 
    theta = math.atan2(drone.velocity.y, drone.velocity.x)
    x1 = drone.position.x
    y1 = drone.position.y
    x2 = math.cos(theta)* 300 + x1
    y2 = math.sin(theta)* 300 + y1

    m = (y2-y1)/(x2-x1)
    def f(x):
        return y1+m*(x-x1)
    def test(x,y,tol):
        return abs(y-f(x)) <= tol

    Fire = False
    Safe = True
    for enemy in enemydrones:
        if test(enemy.position.x, enemy.position.y, 300):
            if target_in_range(enemy.position.x, drone.position.x, RANGE):
                if target_in_range(enemy.position.y, drone.position.y, RANGE):
                    if vel_target(drone.velocity.x, drone.velocity.y, drone.position.x, drone.position.y, enemy.position.x, enemy.position.y):
                        Fire = True

        for friendly in friendlydrones:
            if test(friendly.position.x, enemy.position.y, 10):
                Safe = False

    y = random.randint(1,5)
    if Fire == True and Safe == True and y == 1:
        build_bullet(drone)


#check velocities
def vel_target(vx, vy, dx, dy, ex, ey):
    if vx > 0 and vy > 0:
        if ex > dx or ey > dy:
            return True
    if  vx < 0 and vy > 0:
        if ex < dx or ey > dy:
            return True
    if vx < 0 and vy < 0:
        if ex < dx or ey < dy:
            return True
    if vx > 0 and vy < 0:
        if ex > dx or ey < dy:
            return True
    return False


#Check to see if within range
def target_in_range(x,y,num):
    if x > 0 and y > 0:
        if abs(x - y) < num:
            return True
    elif x > 0 and y < 0:
        if abs(x + y) < num:
            return True
    elif x < 0 and y > 0:
        if abs(x + y) < num:
            return True
    elif x < 0 and y < 0:
        if abs(x - y) < num:
            return True
    return False


# Create simulation boundaries 
def simulate_wall(drone):
    if drone.position.x < WALL:
        drone.velocity.x += WALL_FORCE
    elif drone.position.x > WIDTH - WALL:
        drone.velocity.x -= WALL_FORCE

    if drone.position.y < WALL:
        drone.velocity.y += WALL_FORCE
    elif drone.position.y > HEIGHT - WALL:
        drone.velocity.y -= WALL_FORCE



#Check to see if the drone is out of the bounds
def outofbounds(drone, drones):
    check = False
    if drone.position.x < 0:
        check = True 
    elif drone.position.x > WIDTH:
        check = True 
    elif drone.position.y < 0: 
        check = True 
    elif drone.position.y > HEIGHT:
        check = True

    if check == True:
        drones.remove(drone)
        print "Out of bounds"


#detect if drone is hit by a bullet
def killed(drone, bullet_list):
    for bullet in bullet_list:
        if drone.position.y > bullet.position.y - 2:
            if drone.position.y < bullet.position.y + 2:
                if drone.position.x > bullet.position.x - 2:
                    if drone.position.x < bullet.position.x + 2:
                        if(bullet.team is drone.real_color):
                            print "Death by friendly fire"
                        else:
                            print "Death by enemy fire"
                        bullet.death()
                        return True
    return False


#detect if a drone on drone collision occurs
def collision(curr_drone, drones):
    for drone in drones:
        if curr_drone.position.y > drone.position.y - 3:
            if curr_drone.position.y < drone.position.y + 3:
                if curr_drone.position.x > drone.position.x - 3:
                    if curr_drone.position.x < drone.position.x + 3:
                        #If there is a collision then remove both of the drones
                        drones.remove(drone)
                        print "Death by Collision"
                        return True
    return False
            

#Avoid running into the enemy drone swarm 
def detect_enemy(curr_drone, enemydrones):
    theta = math.atan2(curr_drone.velocity.y, curr_drone.velocity.x)
    x1 = curr_drone.position.x
    y1 = curr_drone.position.y
    x2 = math.cos(theta) * 300 + x1
    y2 = math.sin(theta) * 300 + y1

    m = (y2 - y1) / (x2 - x1)
    def f(x):
        return y1 + m*(x - x1)
    def test(x,y,tol):
        return abs(y-f(x)) <= tol

    for enemy in enemydrones:
        if test(enemy.position.x, enemy.position.y, 90):
            if target_in_range(enemy.position.x, curr_drone.position.x, 20):
                if target_in_range(enemy.position.y, curr_drone.position.y, 20):
                    if vel_target(curr_drone.velocity.x, curr_drone.velocity.y, curr_drone.position.x, curr_drone.position.y, enemy.position.x, enemy.position.y):
                        r = random.randint(0,1)
                        if (r == 1):
                            curr_drone.velocity.x += TURN_AROUND
                        else:
                            curr_drone.velocity.y += TURN_AROUND
































