#The config file declares the constraints for the simulation

#Have the drones fire or not
battle_on = True


#Number of blue drones
blue_drones = 16 

#behavior options: FLOCKING, SELECT_NEAREST, ASSIGN_NEAREST, RABBIT
blue_drone_behavior = ['ASSIGN_NEAREST' if x<blue_drones-1 else 'RABBIT' for x in range(blue_drones)]


#blue_brain = 'FLOCKING'
#blue_rabbit = True
#blue_rabbit_brain = 'RABBIT'


#Number of red drones
red_drones = 16

red_drone_behavior = ['ASSIGN_NEAREST' if x<red_drones/2 else 'SELECT_NEAREST' for x in range(red_drones)]

#red_brain = 'FLOCKING'
#red_rabbit = True
#red_rabbit_brain = 'RABBIT'


#Other simulation constraints

#Furthest range drones can detect and fire
firing_range = 300

#dimensions of the simulation in meters
height = 1000
width = 1000

#Screen update rate
frames_per_sec = 40
simspeed = 2000
wall = 100
wall_force = 50
speed_limit = 300
avoidance_speed = 80
