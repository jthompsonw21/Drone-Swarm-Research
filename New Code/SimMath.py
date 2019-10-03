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


def move(red_drones, blue_drones):
    for drone in red_drones:
        simulate_wall(drone)
        detect_enemy(drone, blue_drones)
        if drone.behavior = RABBIT:
            drone.RABBIT(red_drones,blue_drones, TwoD(900,300))
        else:
            drone.behavior.(red_drones,blue_drones)

        if FIRE:
            fire(drone, red_drones, blue_drones)
        drone.move()


        outofbounds(drone,red_drones)






