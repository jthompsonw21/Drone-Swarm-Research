import config as c

red_behavior  = c.red_drone_behavior
blue_behavior = c.blue_drone_behavior

TIME = something #fix this eventually 

#for now just using arbitrary numbers 
if TIME < 20:
    red_behavior = "rabbit"
elif TIME < 40:  
    red_behavior = "ASSIGN_NEAREST"

def brain_select_execute(drone, red_drones, blue_drones):
    #we can selected between several different behavior types
    #Behaviors can be a combination of brain types
    code here 


#Behaviors
def rabbt_with_hold_and_wait(drone, red_drones, blue_drones):
    if TIME < 5: 
        blue_behavior

