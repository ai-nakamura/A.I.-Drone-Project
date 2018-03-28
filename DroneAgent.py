

class DroneAgent:
    position = "0,0,0"

    def __init__(self, x, y, z, name):
        self.altitude = z
        self.x = x
        self.y = y
        self.name = name
        self.radius = 1
        self.goalFound = False

    def getAgentPosition(self):
        return self.x, self.y, self.altitude

    def setPosition(self, newX, newY, newAlt):
        self.x, self.y, self.altitude = newX, newY, newAlt
        print "new position: " + str(self.getAgentPosition())

    '''
    Scans the terrain around the Drone on the same plane. The resulting scan will have an 'xx'
    to indicate that the Drone has scanned past the edge of the map.
    If 'WA'(water) is found in the scan result, set self.goalFound = True
    '''
    def detectTerrain(self, env):
        print "scanning terrain..."
        print "position: " + str(self.getAgentPosition())
        scanRange = self.radius*2+1
        scan = [['__' for _ in range(scanRange)] for _ in range(scanRange)]
        mapY = self.y - self.radius
        for i in range(scanRange):
            mapX = self.x - self.radius
            for j in range(scanRange):
                data = env.locationData(self.name, mapX, mapY, self.altitude)
                if data != "over edge":
                    scan[j][i] = data
                else:
                    scan[j][i] = 'xx'
                mapX += 1
            mapY += 1

        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in scan]))
        print "\n"
        for i in scan:
            for j in i:
                if j == 'WA':
                    print("Water found!")
                    self.goalFound = True


    '''
    Movement for Drone. Allows for Drone to move freely in all x y z directions.
    Assume that Engine will not try to move Drone to a position with an obstacle already in it
    'speed' will determine how far the Drone can move in one turn, and provides flexibility for
    later implementations of faster Drones 
    '''
    def moveAgent(self, x, y, altitude, speed=1):
        # print "Agent: attempting move to location ", (x, y, altitude)
        newX = self.x + x
        newY = self.y + y
        newAltitude = self.altitude + altitude
        if (newX < 0) | (newX > 9) | (newY < 0) | (newY > 9) | (newAltitude < 0) | (newAltitude > 2): # <- am hard coding environment dimensions here. need to fix
            print ("Agent: cannot move here, out of bounds")
            return False
        self.setPosition(newX, newY, newAltitude)
        print "Agent: moved successfully moved to ", (self.getAgentPosition())
        return True
