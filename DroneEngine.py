
from random import randint
from DroneEnvironment import *
from DroneAgent import *
#from sample import *


class DroneEngine():

    def __init__(self, environment, bee):

        # environment solo test
        '''
        env.printMap()

        drone = 'Be'
        x, y = 0, 0
        altitude = 0

        # drone initial placement testing
        env.updateMap(drone, x, y, altitude, start=True)
        env.printMap()

        # updateMap testing
        x, y = 1, 1
        altitude = 0
        env.updateMap(drone, x, y, altitude)
        env.printMap()

        # collision testing
        # x, y, altitude = 5, 5, 2
        # env.updateMap(drone, x, y, altitude)

        # locationData scan testing
        print (env.locationData(drone, x, y, altitude))
        '''


        # environment + drone test

        # place drone in environment
        beeX, beeY, beeAltitude = bee.getAgentPosition()
        env.updateMap(bee.name, beeX, beeY, beeAltitude, True)

        # environment received drone
        env.printMap()

        # bee terrain detection
        bee.detectTerrain(env)

        # update map and drone on drone's new position until 'WA' found
        steps = 0
        wallBumps = 0
        while (not bee.goalFound) | steps < 500 :
            # if env.collision == False, update agent + map
            newCoord = (bee.x+randint(-10, 10), bee.y+randint(-10, 10), bee.altitude+randint(-5, 1))
            workingCoord = self.normalizeCoord(bee, *newCoord)
            if not env.collision(*workingCoord):
            # I should really write my own method for checking out of bounds on the Engine side.
                if bee.moveAgent(*workingCoord):      # <-- this unpacks tuples for use in arguments! neat!
                    env.updateMap(bee.name, *bee.getAgentPosition())
                    env.printMap()
                else:
                    wallBumps += 1
                    print "Wall bump count: ", wallBumps
            steps += 1
            print "Step count: ", steps
            print (bee.getAgentPosition())
            print ("\n")
        print "Congratulations! It only took ", steps, " steps to complete the mission!"
        print "I mean yea you bumped into the wall ", wallBumps, " times, but you still did it!"
        # check new terrain
        # bee.detectTerrain(env)

        # reminder to write algorithm to regenerate bee location if there's an obstacle already there
        # also need to figure out how we're going to keep weighted data
        # how the hell are we going to do the learning??
        # make the environment or engine figure out a* and a heuristic for drone to compare it to
        # whats a performance metric again? I know we need it somewhere

        # Engine will be doing the moving of the agent around on the map,
        # so if the Map says that the drone can't move there, then Engine won't allow Drone to move
    '''

    Ultimately, we want the Drone to figure out that moving in a direction where the tiles change is more favorable to finding water
    on __init__ self.tileWeights = {}
    def run(self, environment, drone):
        1) randomly choose location to place drone that isn't blocked by an obstacle
        2) while Drone.goalFound == False:
            if (current tile != in tileWeights): add current tile to tileWeights with weight 0.01 -> will only reach during first few runs
            
            # if not on ground layer, move down first
            check level below to see if there's an object beneath (i.e. can't move down)
                if yes, move in the direction it was going and try again -> inefficient in that it doesn't move diagonal down
            scan ground
            pick a direction to move drone to along same plane
                -> direction is determined by (tileWeight data + random value between 0 and 1) -> allows drone to fly to new paths
            if desired spot has object: move up
                if can't move up: move diagonal left
                    if can't more left: move right
                        -> no case for if can't move in either spot. Hopefully won't be an issue.
                -> may have to add 'wall' object to give meaning to the idea of going over an object rather than choosing to go around it
            numSteps++
        3) when Drone.goalFound == True:
            log which tile it ended on (should be 'Cl'(clay))
            read through Drone's log and increase weight of tiles encountered later in it's flight
        
    # Adjusts the weights assigned to each tile located.
    def weightAdjustment(self):
        # example: log = ['st', 'st', 'st', 'st', 'dr', 'gr', 'sa', 'cl']
        1) count how many of each tile
            ex: count = {'st': 4, 'dr': 1, 'gr: 1, 'sa': 1, 'cl': 1}
        for i in tileWeights:
            # arbitrary equation to change weighted values
            tileWeights.get(i) +=  (MU VALUE + +log.index(i)*0.01)/count.get(i) --> MU for now will be 0.2 
            # example: when i = 'st' -> (tileWeights.get('st') == 0.1) += 0.2+((log.index('st') == 0) *0.01)/(count.get('st') == 4)
            #                           = 0.1 + (0.2 + (0*0.01))/4 = 0.1 + 0.2/4 = 0.1 + 0.05 = 0.15
            #          when i = 'dr'   =  = 0.1 + (0.2 + (4*0.01))/1 = 0.1 + (0.2 + 0.04)/1 = 0.1 + 0.24 = 0.34
            #          when i = 'cl'   = 0.1 + (0.2 + (7*0.01))/1 = 0.1 + (0.2 + 0.07)/1 = 0.1 + 0.27 = 0.37 
            #                   weights = 'st' < 'gr' < 'cl'           
        
        
    '''
    def normalizeCoord(self, Drone, x, y, altitude, speed=1):
        # normalize (x, y, altitude) with (-1, 0, 1), then multiply with speed
        normal = [x, y, altitude]
        for i in normal:
            if i > 0:
                normal[normal.index(i)] = 1 * speed
            elif i < 0:
                normal[normal.index(i)] = -1 * speed
            else:
                normal[normal.index(i)] = 0 * speed
        # print "Agent: Normalized values to move this much in each axis: ", (normal[0], normal[1], normal[2])
        # check if agent is trying to move out of bounds
        newX = Drone.x + normal[0]
        newY = Drone.y + normal[1]
        newAltitude = Drone.altitude + normal[2]
        return (newX, newY, newAltitude)




env = DroneEnvironment()
beeName = 'Be'
bee = DroneAgent(0, 0, 0, beeName)
eng = DroneEngine(env, bee)

'''
performance metric
heuristic
'''