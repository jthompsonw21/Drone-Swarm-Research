#The config file declares the constraints for the simulation

#Have the drones fire or not
battle_on = True


#Number of blue drones
blue_drones = 10


#behavior options: FLOCKING, SELECT_NEAREST, ASSIGN_NEAREST, RABBIT, SPLIT_FORMATION
blue_drone_behavior = [ 'ASSIGN_NEAREST' for x in range(blue_drones)]
#blue_drone_behavior = [ 'RABBIT' if x < 3 else 'SPLIT_RABBIT' if x < 6 else 'ASSIGN_NEAREST' for x in range(blue_drones)]


#Make the drone invincible
blue_invincible = False


#Decide whether to use hybrid behavior or not. List is: 
b0 = 'rabbit_with_hold_and_wait'
b1 = 'rabbit_to_assign_nearest'
b2 = 'rabbit_hnw_to_assign_nearest'
b3 = 'rabbit_hnw_to_an_to_sn'
b4 = 'split_formation'

blue_hybrid_behavior = False



#Number of red drones
red_drones = 20
red_drone_behavior = ['SELECT_NEAREST' for x in range(red_drones)]
#red_drone_behavior = [ 'RABBIT' if x == 0 else 'ASSIGN_NEAREST' for x in range(red_drones)]
#Make the drone invincible
red_invicible = False

red_hybrid_behavior = False



#Bullet speed 
bullet_speed = 2000


#Other simulation constraints

#Furthest range drones can detect and fire
firing_range = 300
runaway_enabled = False

#Amount of times we want the simulation to repeat
repeat = 2

#dimensions of the simulation in meters
#make the simulation a cube
height = 700
width = 700
ceiling = 700

#draw height outlines for drones and bullets?
DRONE_OUTLINE = True
BULLET_OUTLINE = False


#Drone z axis flight characteristics
#multiplier for when drone is in descent (typically want >1 multiplier)
descentMultiplier = 1
#multiplier for when drone is in ascent (typically want <1 multiplier)
ascentMultiplier = 1



#Screen update rate
frames_per_sec = 60
simspeed = 2000  #normally 2000
wall = 100
wall_force = 75
speed_limit = 300
speed_min = 130
avoidance_speed = 80
