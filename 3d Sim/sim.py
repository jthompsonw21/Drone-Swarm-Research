import random
import math
import timeit
import config as c
import sys
from SmartDrone import SmartDrone

from Tkinter import *
import SimMath as smath

WIDTH  = c.height
HEIGHT = c.width
CEILING = c.ceiling
FRAMES_PER_SEC = c.frames_per_sec
SIMSPEED = c.simspeed

#How many of each drone there is 
BLUE_DRONES_AMT = c.blue_drones
RED_DRONES_AMT  = c.red_drones

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
    #startpos for blue is 100x100 from top left corner
    blue_startpos = math.sqrt((100**2)+ (100**2))

    #make the blue drones
    for index in range(BLUE_DRONES_AMT):
        blue_drones.append(SmartDrone(FRAMES_PER_SEC, blue_startpos, "blue", "a", BLUE_BEHAVIOR[index]))

    #startpos for red is (WIDTH-100)**2
    red_startpos = ((WIDTH-100))
    #make the red drones
    for index in range(RED_DRONES_AMT):
        red_drones.append(SmartDrone(FRAMES_PER_SEC, red_startpos, "red", "a", RED_BEHAVIOR[index]))
        
        #print "Red drones being placed at: " + str(((math.sqrt(WIDTH**2 + HEIGHT**2)) - 120))

# Called from mainloop() method as a part of Tkinter. Bulk of calculations are here
def update():
    #if no drones left, prevent the crash
    if((len(red_drones) == 0) or (len(blue_drones) == 0)):
            end_sim()
    graph.after(SIMSPEED / FRAMES_PER_SEC, update)
    draw()
    smath.move(red_drones, blue_drones, bullet_list)


#output results of simulation to file and terminal. Close file and empty lists
def output_results():
    global red_drones
    global blue_drones
    global bullet_list
    stop = timeit.default_timer()
    f = open('OUTPUT.txt', 'a')

    #If game ends in a tie
    #print "Red Drones  = " + str(len(red_drones))
    #print "Blue Drones = " + str(len(blue_drones))
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
    global root
    root.destroy()

#Draw all the drones in their positions
def draw():
    graph.delete(ALL)
    for drone in red_drones:
        drone.draw(graph)
    for drone in blue_drones:
        drone.draw(graph)
    for bullet in bullet_list:
        bullet.draw(graph)
    graph.update()







#################################################################################

#Execute the simulation
if __name__ == '__main__':
        main()











