import random
import math
import timeit
import config as c
import sys

from Tkinter import *
import SimMath

WIDTH  = c.height
HEIGHT = c.width

#Returns the lists of how we want each drone to act in the swarms
BLUE_BEHAVIOR = c.blue_drone_behavior
RED_BEHAVIOR  = c.red_drone_behavior

blue_drones = []
red_drones  = []
bullet_list = []


def main():
    #init the drones and then start the mainloop
    initialize()
    mainloop()


def initialize():
    #Setup simulation variables

    build_drones()
    build_graph()


#Function that builds the GUI environment
def build_graph():
    global graph
    root = Tk()
    root.title("Drone Swarm Simulation")
    x = (root.winfo_screenwidth() - WIDTH) / 2
    y = (root.winfo_screenheight() - HEIGHT) / 2
    root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x , y))

    graph = Canvas(root, width=WIDTH, height=HEIGHT, background="white")
    graph.after(1000 / FRAMES_PER_SEC, update)
    graph.pack()
    global start
    start = timeit.default_timer()


#Make a bullet
def build_bullet(drone):
    bullet_list.append(Bullet(drone, FRAMES_PER_SEC))

#Instantiate the drone swarms 
def build_drones():
    '''
    #make the blue drones
    for index in range(BLUE_DRONES_AMT-1):
        blue_drones.append(SmartDrone(FRAMES_PER_SEC, 150, "blue", "a"))

    if BLUE_RABBIT:
        blue_rabbit = SmartDrone(FRAMES_PER_SEC, 300, "blue", "a")
        blue_rabbit.set_rabbit(True)
        blue_drones.append(blue_rabbit)
    else:
        blue_drones.append(SmartDrone(FRAMES_PER_SEC, 300, "blue", "a"))

    #make the red drones
    for index in range(RED_DRONES_AMT-1):
        red_drones.append(SmartDrone(FRAMES_PER_SEC, 900,  "red", "a"))
    
    #for index in range(RED):
    #   self.blue_drones.append(SmartDrone(FRAMES_PER_SEC, 150, "blue", "a"))

    if RED_RABBIT:
        red_rabbit = SmartDrone(FRAMES_PER_SEC, 800, "red", "a")
        red_rabbit.set_rabbit(True)
        red_drones.append(red_rabbit)
    else:
        red_drones.append(SmartDrone(FRAMES_PER_SEC, 900, "red", "a"))
    '''

    #make the blue drones
    for index in range(BLUE_DRONES_AMT):
        blue_drones.append(SmartDrone(FRAMES_PER_SEC, 150, "blue", "a"))

    #make the red drones
    for index in range(RED_DRONES_AMT):
        red_drones.append(SmartDrone(FRAMES_PER_SEC, 900, "red", "a"))

# Called from mainloop() method as a part of Tkinter. Bulk of calculations are here
def update():
    #if no drones left, prevent the crash
    if((len(red_drones) == 0) or (len(blue_drones) == 0)):
        end_sim()
    graph.after(SIMSPEED / FRAMES_PER_SEC, update)
    draw()
    move()


#output results of simulation to file and terminal. Close file and empty lists
def output_results():
    stop = timeit.default_timer()
    f = open('OUTPUT.txt', 'a')

    #If game ends in a tie
    if(len(red_drones) == 0 and len(blue_drones) == 0):
        f.write('Tie ')
        f.write('0\n')
        print "TIE"

    #If the red drones are eliminated
    elif(len(red_drones) == 0):
        f.write('Blue ')
        f.write(str(len(blue_drones)))
        f.write('\n')
        print "\nBlue Drones win with "
        print len(blue_drones)
        print "left"

    #If the blue drones are eliminated
    elif(len(blue_drones) == 0):
        f.write('Red ')
        f.write(str(len(red_drones)))
        f.write('\n')
        print "\nRed Drones win with "
        print len(red_drones)
        print "left"
    
    blue_drones = []
    red_drones = []
    bullet_list = []

    total_time = stop -start
    print ("Time elapsed: ", total_time)
    f.close()



#end the simulation
def end_sim():
    output_results()
    exit()


#Restart the simulation 
def restart_sim():
    output_results()
    root.restart()


