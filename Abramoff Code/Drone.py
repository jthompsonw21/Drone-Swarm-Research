from TwoD import TwoD

import random
import math
import config as c
#import pyautogui


SPEED_LIMIT = c.speed_limit       # FOR DRONE VELOCITY
RANGE = c.firing_range            # FIRE RANGE

#Drone class: update position based on changes in velocity done by the brain

class Drone:

    #initial drone, color, position, velocity
    def __init__(self,move_divider, startpos, color, team):
        self.velocity = TwoD(0, 0)
        r1 = random.randint(1,100)
        r2 = random.randint(1,100)
        self.position = TwoD(startpos-r1,startpos-r2)
        self.move_divider = move_divider * 5
        self.color = color
        self.real_color = color
        self.assignment = None
        self.assigned = False
        self.distanceToEnemy = TwoD(0,0)
        self.team = team 

    def __init1__(self, move_divider, startpos, color, velocity):
        self.velocity = velocity
        self.position = startpos
        self.color = color
        self.move_divider = move_divider * 5
        self.real_color = color


    #random initial starting values
    def random_start(self, width, height, offset):
        if random.randint(0, 1):
            y = random.randint(1, height)
            if random.randint(0, 1):
                x = -offset
            else:
                x = width + offset
        else:
            x = random.randint(1, width)
            if random.randint(0, 1):
                y = -offset
            else:
                y = height + offset
        return x, y

    #draw drones as circles with lines
    def draw(self, graph):
      theta = math.atan2(self.velocity.y, self.velocity.x)
      centerx = self.position.x
      centery = self.position.y
      x1 = self.position.x + 3
      y1 = self.position.y + 3
      x2 = self.position.x - 3
      y2 = self.position.y - 3

      linex = math.cos(theta) * 7 + centerx
      liney = math.sin(theta) * 7 + centery

      graph.create_oval(x1,y1,x2,y2, fill = self.color)
      graph.create_line(centerx, centery,linex, liney, fill = 'black')


    # Limit drone speed.
    def limit_speed(self):
      if self.velocity.mag() > SPEED_LIMIT:
        self.velocity /= self.velocity.mag() / SPEED_LIMIT

    def CalculateDistanceToEnemy(self, enemydrones):
      centerenemy = TwoD(0,0)
      for drone in enemydrones:
        centerenemy += drone.position
      if len(enemydrones) > 0:
        centerenemy /= (len(enemydrones))

      self.distanceToEnemy = self.distanceToCenter(centerenemy)

    #The Brain of the drone
    #calculate update velocity based on rules of flocking


    def RABBIT(self, drones, enemydrones, DEST):
       self.CalculateDistanceToEnemy(enemydrones)
        #find closest drone using distance formula
       close = TwoD(0, 0)
       list1 = []

       for drone in enemydrones:
          list1.append(self.distance(drone))
       if(len(list1) != 0):
        closest = min(list1)

       #chase enemy based on current position
       for drone in enemydrones:
         if self.distance(drone) == closest:
            close += drone.position
       
       RUNAWAY = False
       if self.position.y>close.y-(RANGE):
         if self.position.y<close.y+(RANGE):
           if self.position.x>close.x-(RANGE):
             if self.position.x<close.x+(RANGE):
              RUNAWAY = True
       if (RUNAWAY == False):
          v1 = (close - self.position) / 2
       else:
          r = random.randint(0,1)
          if r == 0:
            self.color = "white"
          else:
             self.color = self.real_color

          v1 = DEST - self.position 
       self.__temp = v1

    def FLOCKING(self, drones, enemydrones):
         self.CalculateDistanceToEnemy(enemydrones)
         if len(drones) > 1:
              v1 = self.cohesion(drones)
              v2 = self.seperation(drones)
              v3 = self.alignment(drones)
              v4 = self.target_enemy(drones,enemydrones)
              print "v1 = " + str(v1) + "  v2 = " + str(v2) + "  v3 = " + str(v3) + "  v4 = " + str(v4)
              self.__temp = v1 + v2 + v3 + v4
         else:
              v4 = self.target_enemy(drones, enemydrones)
              self.__temp = v4

  
    #target selection brain
    def SELECT_NEAREST(self, drones, enemydrones):
        self.CalculateDistanceToEnemy(enemydrones)
        attack = False
        for enemy in enemydrones:
          if self.position.y>enemy.position.y-RANGE:
            if self.position.y<enemy.position.y+RANGE:
              if self.position.x>enemy.position.x-RANGE:
                if self.position.x<enemy.position.x+RANGE:
                  attack = True

          #do target select, flash red and white
          if(attack):
            r = random.randint(0,1)
            if r == 0:
              self.color = "white"
            else:
              self.color = self.real_color
            v1 = self.target_select(enemydrones)
            self.__temp = v1
          #act normal
          else:
            self.FLOCKING(drones, enemydrones)

    def ASSIGN_NEAREST(self, drones, enemydrones):
        attack = False
        self.CalculateDistanceToEnemy(enemydrones)
        for enemy in enemydrones:
          if self.position.y>enemy.position.y-RANGE:
            if self.position.y<enemy.position.y+RANGE:
              if self.position.x>enemy.position.x-RANGE:
                if self.position.x<enemy.position.x+RANGE:
                  attack = True

        if(attack):
         r = random.randint(0,1)
         if r == 0:
           self.color = "white"
         else:
           self.color = self.real_color
           v1 = self.assign(drones, enemydrones)
           self.__temp = v1
          #act normal
        else:
          self.FLOCKING(drones, enemydrones)

        for enemy in enemydrones:
          enemy.assigned = False
        for drone in drones:
          drone.assignment = None


    #move drone based on updated velocities
    def move(self):
        print "Updating velocity with: " + str(self.__temp)
        self.velocity += self.__temp
        self.limit_speed()
        self.position += self.velocity / self.move_divider

    def assign(self, drones, enemydrones):
       sorted(drones, key=lambda Drone: Drone.distanceToEnemy)
       sorted(enemydrones, key=lambda Drone: Drone.distanceToEnemy)


       for drone in drones:
        for enemy in enemydrones:
          if enemy.assigned == False:
            drone.assignment = enemy
            enemy.assigned = True

       if self.assignment == None:
           self.assignment = enemydrones[0]

       return (self.assignment.position - self.position) / 2

    #chase closest target
    def target_select(self, enemydrones):
       vector = TwoD(0, 0)
       list1 = []
       #find closest drone using distance formula
       for drone in enemydrones:
          list1.append(self.distance(drone))
       closest = min(list1)

       #chase enemy based on current position
       for drone in enemydrones:
         if self.distance(drone) == closest:
            vector += drone.position
       return (vector - self.position) / 2

    #fly to center of mass of the neighbors
    def cohesion(self, drones):
        vector = TwoD(0, 0)
        #using the other positions, calculate average position
        for drone in drones:
            if drone is not self:
                if drone.team == self.team:
                  vector += drone.position
        vector /= (len(drones) +1)
        #return first offset, move 10% of the way to center
        return (vector - self.position) / 8

    #dont get too close together however
    def seperation(self, drones):
        vector = TwoD(0, 0)
        for drone in drones:
            if drone is not self:
               if drone.team == self.team:              
                if (self.position - drone.position).mag() < 45:
                    vector -= (drone.position - self.position)
        return  vector * 1.5

    #try and match velocities with nearby drones
    def alignment(self, drones):
        vector = TwoD(0, 0)
        for drone in drones:
            if drone is not self:
                if drone.team == self.team:              
                 vector += drone.velocity
        vector /= (len(drones) +1)
        return (vector - self.velocity) / 8

    #chase the other flock
    def target_enemy(self, drones, enemydrones):
        vector = TwoD(0, 0)
        for drone in enemydrones:
           vector += drone.position
        vector /= (len(enemydrones)+1)
        return (vector - self.position) / 7.5

    #simply calculate the distance
    def distance(self, enemy):
      x = (self.position.x - enemy.position.x)**2
      y = (self.position.y - enemy.position.y)**2
      return math.sqrt(x + y)

    def distanceToCenter(self, Pos):
      x = (self.position.x - Pos.x)**2
      y = (self.position.y - Pos.y)**2
      return math.sqrt(x + y)
