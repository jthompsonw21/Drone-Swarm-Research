#The config file declares the constraints for the simulation

#Have the drones fire or not
battle_on = False


#Number of blue drones
blue_drones = 10
#behavior options: FLOCKING, SELECT_NEAREST, ASSIGN_NEAREST, RABBIT
blue_drone_behavior = ['SELECT_NEAREST' for x in range(blue_drones)]


#Number of red drones
red_drones = 10
red_drone_behavior = ['RABBIT' if x < 5 else 'ASSIGN_NEAREST' for x in range(red_drones)]

#Other simulation constraints

#Furthest range drones can detect and fire
firing_range = 300

#Amount of times we want the simulation to repeat
repeat = 2

#dimensions of the simulation in meters
#make the simulation a cube 
height = 1300
width = 1300
ceiling = 1300

#Screen update rate
frames_per_sec = 40
simspeed = 2000
wall = 100
wall_force = 50
speed_limit = 300
avoidance_speed = 80
