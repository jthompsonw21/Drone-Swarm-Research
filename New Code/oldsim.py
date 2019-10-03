#import some standard python libraries
import random
import math
import timeit
import config as c
import sys

#import the classes that we made and Tkinter for visuals
from Drone import Drone
from SmartDrone import SmartDrone
from Bullet import Bullet
from Tkinter import *
from TwoD import TwoD


#create global variables retrieved from config files
FIRE = c.battle_on
RED_DRONES_AMT = c.red_drones
BLUE_DRONES_AMT = c.blue_drones
RANGE = c.firing_range
BLUE_BEHAVIOR = c.blue_drone_behavior
RED_BEHAVIOR  = c.red_drone_behavior 
#RED_BRAIN = getattr(SmartDrone, c.red_brain)
#BLUE_BRAIN = getattr(SmartDrone, c.blue_brain)
#BLUE_RABBIT_BRAIN = getattr(SmartDrone, c.blue_rabbit_brain)
#RED_RABBIT_BRAIN = getattr(SmartDrone, c.red_rabbit_brain)
#BLUE_RABBIT = c.blue_rabbit
#RED_RABBIT = c.red_rabbit


#Other required items
WIDTH = c.height
HEIGHT = c.width
WALL = c.wall
WALL_FORCE = c.wall_force
DRONE_RADIUS = 3
OFFSET_START = 20
FRAMES_PER_SEC = c.frames_per_sec
SIMSPEED = c.simspeed
TURN_AROUND = c.avoidance_speed



blue_drones = []
red_drones = []
bullet_list = []


########################################################################################

def main():
    #initialize the drones and start the main loop
    #blue_drones = []
    #red_drones = []

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


#Moves the drones and bullets
def move():
    #Start with the red drones
    for drone in red_drones:
        simulate_wall(drone)
        detect_enemy(drone, blue_drones)
        drone.behavior(drone, red_drones, blue_drones)
        '''
        if drone.is_rabbit == True:
            RED_RABBIT_BRAIN(drone,red_drones, blue_drones, TwoD(900,300))
        else:
            RED_BRAIN(drone, red_drones, blue_drones)
        '''
        
        #Check to see if drones can fire at each other. If so, then fire
        if FIRE:
            fire(drone, red_drones, blue_drones)
        drone.move()

        #Check to see if the current drone is out of bounds 
        outofbounds(drone, red_drones)

        #Check to see if the current drone is killed or collided with an enemy drone
        if(killed(drone) or  collision(drone, blue_drones)):
            red_drones.remove(drone)
            print("Number of red drones left:")
            print len(red_drones)



    #Redo same thing with blue drones
    for drone in blue_drones:
        simulate_wall(drone)
        detect_enemy(drone, red_drones)
        drone.behavior(drone, blue_drones, red_drones)

        '''
        if drone.is_rabbit == True:
            BLUE_RABBIT_BRAIN(drone,blue_drones, red_drones, TwoD(900,300))
        else:
            BLUE_BRAIN(drone, blue_drones, red_drones)
        '''
        if FIRE:
            fire(drone, blue_drones, red_drones)
        drone.move()
        outofbounds(drone, blue_drones)
        if(killed(drone) or  collision(drone, red_drones)):
            blue_drones.remove(drone)
            print("Number of blue drones left:")
            print len(blue_drones)


    #Move bullets or remove 
    for bullet in bullet_list:
        if bullet.alive:
            bullet.move()
        else:
            bullet_list.remove(bullet)


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
        
    
#Fire a bullet if the target is within range. Friendly Fire? 
def fire(drone, drones, enemydrones):
    #If no enemies then return 
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

        for friendly in drones:
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
def killed(drone):
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

                        if curr_drone.real_color == "blue":
                            blue_drones.remove(curr_drone)
                        elif curr_drone.real_color == "red":
                            red_drones.remove(curr_drone)

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



###########################################################################################################

#Execute the simulation
if __name__ == '__main__':
    main()

























    
