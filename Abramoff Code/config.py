###################################
#Yair Abramoff
 #Drone Simulation Research

 #The config file declares the constraints to the
 #Simulation '

#Have the drones fire or not
battle_on = True

#BLUE DRONES
#number
blue_drones = 12
#brain: FLOCKING, SELECT_NEAREST, ASSIGN_NEAREST
blue_brain = 'ASSIGN_NEAREST'
blue_rabbit = True
blue_rabbit_brain = 'RABBIT'

#RED DRONES
#number
red_drones = 12
#brain: FLOCKING, SELECT_NEAREST, ASSIGN_NEAREST
red_brain = 'SELECT_NEAREST'
red_rabbit = False
red_rabbit_brain = 'RABBIT'

######################
#Administrative
#drones effective to aim at/bullets can kill
firing_range = 300

#dimensions of simulation in meters
height = 1000
width = 1000

#Screen update rate
frames_per_sec = 40
simspeed = 2000
wall = 100
wall_force = 50
speed_limit = 300
avoidance_speed = 80
