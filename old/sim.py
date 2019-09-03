import random           # FOR RANDOM BEGINNINGS
import bulletmodule
import math
import dronemodule
import timeit
import config as c 
import sys

from Drone import Drone
from Bullet import Bullet
from Tkinter import *   # ALL VISUAL EQUIPMENT
from TwoD import TwoD


#global declared variables in config file
FIRE =  c.battle_on     
REDDRONES = c.red_drones
BLUEDRONES = c.blue_drones 
RANGE = c.firing_range
red_brain = getattr(Drone, c.red_brain)
blue_brain = getattr(Drone, c.blue_brain)
blue_rabbit_brain = getattr(Drone, c.blue_rabbit_brain)
red_rabbit_brain = getattr(Drone, c.red_rabbit_brain)
BLUE_RABBIT = c.blue_rabbit
RED_RABBIT = c.red_rabbit



#admin 
WIDTH = c.height
HEIGHT = c.width
WALL = c.wall             
WALL_FORCE = c.wall_force
DRONE_RADIUS = 3         # FOR DRONES IN PIXELS
OFFSET_START = 20       # FROM WALL IN PIXELS
FRAMES_PER_SEC = c.frames_per_sec     # SCREEN UPDATE RATE
SIMSPEED = c.simspeed         # CONTROLS SCALING
TURN_AROUND = c.avoidance_speed        # WHEN COLLISION IS DETECTED

################################################################################

def main():
    # Start the program.
    initialise()
    mainloop()

def initialise():
    # Setup simulation variables.
    build_drones()
    build_graph()

def build_graph():
     # Build GUI environment.
    global graph
    root = Tk()
    #root.resizable(False, False)
    root.title('Abramoff Simulation')
    x = (root.winfo_screenwidth() - WIDTH) / 2
    y = (root.winfo_screenheight() - HEIGHT) / 2
    root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))
    root.bind_all('<Escape>', lambda event: event.widget.quit())
    graph = Canvas(root, width=WIDTH, height=HEIGHT, background='white')
    graph.after(1000 / FRAMES_PER_SEC, update)
    graph.pack()
    global start
    start = timeit.default_timer()


#Main simulation loop
def update():
  #if no drones left, prevent the crash
    if(len(dronemodule.reddrones) == 0 or len(dronemodule.bluedrones) == 0):
      end_sim()      
    graph.after(SIMSPEED / FRAMES_PER_SEC, update)
    draw()
    move()

def end_sim():
  stop = timeit.default_timer()
  f = open('OUTPUT.txt', 'a')

  if((len(dronemodule.reddrones) == 0) and (len(dronemodule.bluedrones) == 0)):  
    f.write('Tie ')
    f.write('0\n')
    print "TIE"

  elif(len(dronemodule.reddrones) == 0):
    f.write('Blue ')
    f.write(str(len(dronemodule.bluedrones)))
    f.write('\n')
    print "\nBlue Drones win, drones left "
    print len(dronemodule.bluedrones)
    
  elif(len(dronemodule.bluedrones) == 0):
    f.write('Red ')
    f.write(str(len(dronemodule.reddrones)))
    f.write('\n')
    print "\nRed Drones win, drones left,"
    print len(dronemodule.reddrones)
    
  num = stop - start
  #f.write('Time: ')
  #f.write(str(num))
  #f.write('\n')
  print('Time: ', num)
  f.close()
  exit()


# Move all drones.
def move():
    reddrones = dronemodule.reddrones
    bluedrones = dronemodule.bluedrones 

    #for red drones
    for drone in reddrones:
      simulate_wall(drone)
      detect_enemy(drone, bluedrones) 
      if drone.real_color == "green":
        red_rabbit_brain(drone, reddrones, bluedrones, TwoD(900,300))
      else:
        red_brain(drone, reddrones, bluedrones)      
      if FIRE:
        fire(drone, reddrones, bluedrones)
      drone.move()
      outofbounds(drone, reddrones)
      if (killed(drone) or collision(drone, bluedrones)):
        dronemodule.reddrones.remove(drone)
        print ("Number of Red Drones left "),
        print len(reddrones)

    #for blue drones
    for drone in bluedrones:
      simulate_wall(drone)
      detect_enemy(drone, reddrones)
      if drone.real_color == "green":
        blue_rabbit_brain(drone, bluedrones, reddrones, TwoD(300,900))
      else:
        blue_brain(drone, bluedrones, reddrones)
      if FIRE:
        fire(drone, bluedrones, reddrones)
      drone.move()
      outofbounds(drone, bluedrones)
      if (killed(drone) or collision(drone, reddrones)):
        bluedrones.remove(drone)
        print ("Number of Blue Drones left "),
        print len(bluedrones)

    for bullet in bulletmodule.bulletList:
      if bullet.alive:
        bullet.move()
      else:
        bulletmodule.bulletList.remove(bullet)


# Draw all drones in position
def draw():
    graph.delete(ALL)
    for drone in dronemodule.reddrones:
       drone.draw(graph)
    for drone in dronemodule.bluedrones:
       drone.draw(graph)
    for bullet in bulletmodule.bulletList:
       bullet.draw(graph)
    graph.update()

#fire the bullet if target close, friendly fire
def fire(drone, drones, enemydrones):
    theta = math.atan2(drone.velocity.y, drone.velocity.x)
    x1 = drone.position.x
    y1 = drone.position.y
    x2 = math.cos(theta) * 300 + x1
    y2 = math.sin(theta) * 300 + y1

    m = (y2 - y1) / (x2 - x1)
    def f(x): 
      return y1 + m*(x-x1) 
    def test(x,y,tol):
      return abs(y-f(x)) <= tol

    Fire = False
    Safe = True
    if len(enemydrones) == 0: 
      return
    for enemy in enemydrones:
      if test(enemy.position.x, enemy.position.y, 300):
        if target(enemy.position.x, drone.position.x, RANGE):
          if target(enemy.position.y, drone.position.y, RANGE):
            if vel_target(drone.velocity.x,drone.velocity.y,drone.position.x,drone.position.y,enemy.position.x,enemy.position.y):
             Fire = True
    for friendly in drones:
      if test(friendly.position.x, enemy.position.y, 10):
        Safe = False
    
    y = random.randint(1,5)
    if Fire == True and Safe == True and y == 1:
       build_bullet(drone)

#check velocities
def vel_target(vx, vy, dx,dy, ex,ey):
  if vx > 0 and vy > 0:
    if ex > dx or ey > dy:
      return True
  if vx < 0 and vy > 0:
    if ex < dx or ey > dy:
      return True
  if vx < 0 and vy < 0:
    if ex < dx or ey < dy:
      return True
  if vx > 0 and vy < 0:
    if ex > dx or ey < dy:
      return True
  return False

#check to see if within range
def target(x,y,num):
  #print num
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

#create a bullet, add to bullet list with initial drone location
def build_bullet(drone):
  bulletmodule.bulletList.append(Bullet(drone, FRAMES_PER_SEC))  

def build_drones1():
  dronemodule.bluedrones.append(Drone(FRAMES_PER_SEC, TwoD(200,200), "blue",
    TwoD(500, -50)))
  dronemodule.reddrones.append(Drone(FRAMES_PER_SEC, TwoD(400,400), "red",
    TwoD(-50, -500)))

  
        
#create the drones list, calling drone class
def build_drones():
  for index in range(BLUEDRONES-1):
    dronemodule.bluedrones.append(Drone(FRAMES_PER_SEC, 150, "blue","a")) 
  
  if BLUE_RABBIT:
    dronemodule.bluedrones.append(Drone(FRAMES_PER_SEC, 300, "green", "a"))
  else:
    dronemodule.bluedrones.append(Drone(FRAMES_PER_SEC, 150, "blue", "a"))


  for index in range(REDDRONES/2):
    dronemodule.reddrones.append(Drone(FRAMES_PER_SEC, 750, "red","a"))

  
  for index in range(REDDRONES / 2 , REDDRONES-1):
    dronemodule.reddrones.append(Drone(FRAMES_PER_SEC, 900, "red","b")) 

  if RED_RABBIT:
    dronemodule.reddrones.append(Drone(FRAMES_PER_SEC, 800, "green", "a"))
  else:
    dronemodule.reddrones.append(Drone(FRAMES_PER_SEC, 900, "red","a"))



# Create simulation boundaries.
def simulate_wall(drone):
    if drone.position.x < WALL:
        drone.velocity.x += WALL_FORCE
    elif drone.position.x > WIDTH - WALL:
        drone.velocity.x -= WALL_FORCE
    if drone.position.y < WALL:
        drone.velocity.y += WALL_FORCE
    elif drone.position.y > HEIGHT - WALL:
        drone.velocity.y -= WALL_FORCE

# Create simulation boundaries.
def outofbounds(drone, drones):
    if drone.position.x < 0:
        drones.remove(drone)
        print ("Out of bounds")
    elif drone.position.x > WIDTH:
        drones.remove(drone)
        print ("Out of bounds")  
    if drone.position.y < 0:
        drones.remove(drone)
        print ("Out of bounds")
    elif drone.position.y > HEIGHT:
        drones.remove(drone)
        print ("Out of bounds")

#create the bullet list, calling bullet list
def build_bullets():
  bulletmodule.bulletList = []

#avoid running into enemy drones
def detect_enemy(me, enemydrones):
  theta = math.atan2(me.velocity.y, me.velocity.x)
  x1 = me.position.x
  y1 = me.position.y
  x2 = math.cos(theta) * 300 + x1
  y2 = math.sin(theta) * 300 + y1

  m = (y2 - y1) / (x2 - x1)
  def f(x): 
    return y1 + m*(x-x1) 
  def test(x,y,tol):
    return abs(y-f(x)) <= tol

  for enemy in enemydrones:
    if test(enemy.position.x, enemy.position.y, 90):
        if target(enemy.position.x, me.position.x, 20):
          if target(enemy.position.y, me.position.y, 20):
            if vel_target(me.velocity.x,me.velocity.y,me.position.x,me.position.y,enemy.position.x,enemy.position.y):
              r = random.randint(0,1)
              if (r == 1):
                me.velocity.y += TURN_AROUND
              else:
                me.velocity.y -= TURN_AROUND


#detect if there is a drone on drone collision
def collision(me, drones):
  for drone in drones: 
    if me.position.y>drone.position.y-2:
      if me.position.y<drone.position.y+2:
       if me.position.x>drone.position.x-2:
        if me.position.x<drone.position.x+2:
          drones.remove(drone)
          print "Death by Collision"
          return True
  return False

#detect if hit by bullet
def killed(me):
  for bullet in bulletmodule.bulletList:
    if me.position.y>bullet.position.y-2:
      if me.position.y<bullet.position.y+2:
       if me.position.x>bullet.position.x-2:
        if me.position.x<bullet.position.x+2:
          if(bullet.team is me.real_color):
            print 'Death by Friendly Fire'
          else:
            print 'Death by Enemy Fire'
          bullet.death()
          return True
  return False




################################################################################

# Execute the simulation.
if __name__ == '__main__':
    main()
