#import some standard python libraries
from __future__ import division
import random
import math
import  timeit
import config as c
import sys

#import the classes that we need for visuals
from Drone import Drone
from SmartDrone import SmartDrone
from Bullet import Bullet
from ThreeD import ThreeD

FIRE = c.battle_on
RED_DRONES_AMT  = c.red_drones
BLUE_DRONES_AMT = c.blue_drones
RANGE = c.firing_range
BLUE_BEHAVIOR = c.blue_drone_behavior
RED_BEHAVIOR  = c.red_drone_behavior
WIDTH = c.height
HEIGHT = c.width
CEILING = c.ceiling
WALL = c.wall
WALL_FORCE = c.wall_force
DRONE_RADIUS = 3
OFFSET_START = 20
FRAMES_PER_SEC = c.frames_per_sec
SIMSPEED = c.simspeed
TURN_AROUND = c.avoidance_speed


#Moves the drones and bullets
def move(red_drones, blue_drones, bullet_list):
    for drone in red_drones:
        simulate_wall(drone)
        detect_enemy(drone, blue_drones)
        drone.behavior(drone, red_drones, blue_drones)

        #Check to see if drones can fire at each other. If so, then fire
        if FIRE:
            fire(drone, red_drones, blue_drones, bullet_list)
        drone.move()

        #Check to see if the current drone is out of bounds
        outofbounds(drone,red_drones)

        #print(str(drone.real_color) + "Drone position: " + str(drone.position))

        #Check to see if the current drone is killed or collided with an enemy drone
        if(killed(drone, bullet_list) or collision(drone, blue_drones)):
            drone.assigned = None
            red_drones.remove(drone)
            print("Number of red drones left: ")
            print(len(red_drones))


    #Redo same thing with blue drones
    for drone in blue_drones:
        simulate_wall(drone)
        detect_enemy(drone, red_drones)
        drone.behavior(drone, blue_drones, red_drones)

        if FIRE:
            fire(drone, blue_drones, red_drones, bullet_list)
        drone.move()
        outofbounds(drone, blue_drones)

        #print(str(drone.real_color) + "Drone position: " + str(drone.position))
        if(killed(drone, bullet_list) or  collision(drone, red_drones)):
            drone.assigned = None
            blue_drones.remove(drone)
            print("Number of blue drones left:")
            print(len(blue_drones))


    #Move bullets or remove
    for bullet in bullet_list:
        if bullet.alive:
            bullet.move()
        else:
            bullet_list.remove(bullet)


#Fire a  bullet if the target is within range. Friendly Fire?
def fire(drone, friendlydrones, enemydrones, bullet_list):
    #If no enemies left then return
    if len(enemydrones) == 0:
        return
    if drone.fire(friendlydrones, enemydrones, RANGE) == True:
        build_bullet(bullet_list, drone)


#create a bullet, add to bullet list with initial drone location
def build_bullet(bullet_list,  drone):
    bullet_list.append(Bullet(drone,FRAMES_PER_SEC))


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

    if drone.position.z < WALL:
        drone.velocity.z += WALL_FORCE
    elif drone.position.z > WIDTH - WALL:
        drone.velocity.z -= WALL_FORCE



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
    elif drone.position.z < 0:
        check = True
    elif drone.position.z > CEILING:
        check = True
    elif drone.position.z < 0:
        check = True

    if check == True:
        drones.remove(drone)
        print("Out of bounds")


#detect if drone is hit by a bullet
def killed(drone, bullet_list):
    if drone.invincible == True:
        return False
    for bullet in bullet_list:
        if drone.position.y > bullet.position.y - 2:
            if drone.position.y < bullet.position.y + 2:
                if drone.position.x > bullet.position.x - 2:
                    if drone.position.x < bullet.position.x + 2:
                        if drone.position.z > bullet.position.z - 2:
                            if drone.position.z < bullet.position.z + 2:
                                if(bullet.team is drone.real_color):
                                    print("Death by friendly fire")
                                else:
                                    print("Death by enemy fire")
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
                        if curr_drone.position.z  > drone.position.z - 3:
                            if curr_drone.position.z < drone.position.z + 3:
                                #If there is a collision then remove both of the drones
                                drones.remove(drone)
                                print("Death by Collision")
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
                    if vel_target(curr_drone.velocity.x, curr_drone.velocity.y,curr_drone.velocity.z, curr_drone.position.x, curr_drone.position.y, curr_drone.position.z, enemy.position.x, enemy.position.y, enemy.position.z):
                        r = random.randint(0,1)
                        if (r == 1):
                            curr_drone.velocity.x += TURN_AROUND
                        else:
                            curr_drone.velocity.y += TURN_AROUND
