import drone_brains 


def brain_select_execute(red_drones, blue_drones, red_hybrid_behavior, blue_hybrid_behavior, time):
    #we can selected between several different behavior types
    #Behaviors can be a combination of brain types
    if red_hybrid_behavior != False:
        red_drones = getattr(Behavior, red_hybrid_behavior)(red_drones, time)
    if blue_hybrid_behavior != False:
        blue_drones = getattr(Behavior, blue_hybrid_behavior)(blue_drones, time)
    
    return red_drones, blue_drones




#############################################################
######################### Behaviors #########################
#############################################################
class Behavior:

    '''
    For the first 5 seconds of the simulation, the RABBITs in 
    the drone swarm distract the enemy swarm while the non-rabbits
    stay behind in a holding pattern. Once the 5 seconds are over, 
    the non-rabbits proceed to attack the enmy swarm.
    '''
    def rabbit_with_hold_and_wait(drones, time):
        for i in range(len(drones)):
            if drones[i].behavior == getattr(drone_brains, 'RABBIT'):
                continue
            else:
                if time < 7:
                    drones[i].behavior = getattr(drone_brains, 'HOLD_AND_WAIT')
                    drones[i].behavior_name = 'HOLD_AND_WAIT'
                else:
                    drones[i].behavior = getattr(drone_brains, 'ASSIGN_NEAREST')
                    drones[i].behavior_name = 'ASSIGN_NEAREST'
        return drones


    '''
    For the first 5 seconds the rabbits in the swarm distract the 
    enemy swarm while the others attack. After 5 seconds the rabbits 
    join in to attach using ASSIGN_NEAREST attack method.
    '''
    def rabbit_to_assign_nearest(drones, time):
        for i in range(len(drones)):
            if drones[i].behavior == getattr(drone_brains, 'ASSIGN_NEAREST'):
                continue
            else:
                if time > 5:
                    drones[i].behavior = getattr(drone_brains, 'ASSIGN_NEAREST')
                else:
                    drones[i].behavior = getattr(drone_brains, 'RABBIT')
        return drones


