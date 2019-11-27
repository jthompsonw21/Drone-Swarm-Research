#The config file declares the constraints for the simulation

#Have the drones fire or not
battle_on = True


#Number of blue drones
blue_drones = 15
#behavior options: FLOCKING, SELECT_NEAREST, ASSIGN_NEAREST, RABBIT
blue_drone_behavior = [ 'RABBIT' if x == 0 else 'ASSIGN_NEAREST' for x in range(blue_drones)]
#Make the drone invincible
blue_invincible = False


#Decide whether to use hybrid behavior or not. List is: 
#'rabbit_with_hold_and_wait'
#'rabbit_to_assign_nearest'
#'rabbit_hnw_to_assign_nearest'
blue_hybrid_behavior = 'rabbit_hnw_to_assign_nearest'



#Number of red drones
red_drones = 15
red_drone_behavior = ['SELECT_NEAREST' for x in range(red_drones)]
#red_drone_behavior = [ 'RABBIT' if x == 0 else 'ASSIGN_NEAREST' for x in range(red_drones)]
#Make the drone invincible
red_invicible = False

red_hybrid_behavior = False



#Bullet speed 
bullet_speed = 2000


#Other simulation constraints

#Furthest range drones can detect and fire
firing_range = 400

#Amount of times we want the simulation to repeat
repeat = 2

#dimensions of the simulation in meters
#make the simulation a cube
height = 700
width = 700
ceiling = 700

#draw height outlines for drones and bullets?
DRONE_OUTLINE = True
BULLET_OUTLINE = True


#Drone z axis flight characteristics
#multiplier for when drone is in descent (typically want >1 multiplier)
descentMultiplier = 1
#multiplier for when drone is in ascent (typically want <1 multiplier)
ascentMultiplier = 1



#Screen update rate
frames_per_sec = 40
simspeed = 2000
wall = 100
wall_force = 50
speed_limit = 300
avoidance_speed = 80
