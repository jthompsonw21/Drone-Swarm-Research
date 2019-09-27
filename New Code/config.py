#The config file declares the constraints for the simulation

#Have the drones fire or not
battle_on = True


#Number of blue drones
blue_drones = 12

#brain options: FLOCKING, SELECT_NEAREST, ASSIGN_NEAREST
blue_brain = 'FLOCKING'
blue_rabbit = True
blue_rabbit_brain = 'RABBIT'


#Number of red drones
red_drones = 12

red_brain = 'FLOCKING'
red_rabbit = True
red_rabbit_brain = 'RABBIT'


#Other simulation constraints

#Furthest range drones can detect and fire
firing_range = 300

#dimensions of the simulation in meters
height = 800
width = 800

#Screen update rate
frames_per_sec = 40
simspeed = 2000
wall = 100
wall_force = 50
speed_limit = 300
avoidance_speed = 80
