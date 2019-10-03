import arcade as a
from SmartDrone import SmartDrone
import timeit
import config as c
import sys
import SimMath

SCREEN_WIDTH  = c.height
SCREEN_HEIGHT = c.width 

#Returns the lists of how we wnat each drone to act in the swarms
BLUE_BEHAVIOR = c.blue_drone_behavior
RED_BEHAVIOR = c.red_drone_behavior


blue_drones = []
red_drones  = []
bullet_list = []

def main():
    #init the drones an then start the mainloop
    initialize()
    #mainloop() or whatever it is for arcade package

def initialize()
    #Setup simulation variables
    build_drones()
    create_gui()


#Instantiate the drone swarms
def build_drones():
    #make the blue drones
    for index in range(BLUE_DRONES_AMT):
        blue_drones.append(SmartDrone(FRAMES_PER_SEC, 150, "blue", "a"))

    #make the red drones
    for index in range(RED_DRONES_AMT):
        red_drones.append(SmartDrone(FRAMES_PER_SEC, 900, "red", "a"))





def create_gui():
    a.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Drone Swarm Simulation")
    a.start_render()
    

