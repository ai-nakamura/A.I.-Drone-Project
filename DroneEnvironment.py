"""
The Environment

A 3 tiered environment for the drone to explore.

Contains at least one and no more than 5 of each of the following:
Bush (up to Ground level)
Tree (up to Mid level)
Mountain (up to Sky level)
They are stored in self.obstacles as ('BU', 1), ('TR', 2), ('MO', 3)
then placed into self.objects as {('BU', 1) : [(x1, y1), (x2, y2), ..., (xN, yN)]}
where N is the number of existing objects of that type.
There is a separate dictionary for each layer

The Ground types that will be used, in order of layers of being near water:
Clay = 1 layer around water
Sand = 2 
Grass =3
Dirt = 4
Stone = 5+
stored in self.groundTypes as ('cl', 1), ('sa',2), ('gr',3), ('dr',4), ('st',5)

The goal state water ('WA', 0) is stored in self.groundTypes for ground placement,
then placed in self.objects for map info storage
"""

from random import randint

class DroneEnvironment:
    def __init__(self):
        self.obstacles = [('BU', 1), ('TR', 2), ('MO', 3)]
        self.groundTypes = [('WA',0),('cl', 1), ('sa',2), ('gr',3), ('dr',4), ('st',5)]
        self.objects = [{},{},{}]
        self.width, self.height = 10, 10
        self.sky    = [[('__',) for x in range(self.width)] for y in range(self.height)]
        self.mid    = [[('__',) for x in range(self.width)] for y in range(self.height)]
        self.ground = [[self.groundTypes[5] for x in range(10)] for y in range(10)] #start all ground as 'st'
        self.layer  = [self.ground, self.mid, self.sky]
        self.fillGround()
        self.fillObstacles()

    def printMap(self):
        print("printing environment map")
        for l in self.layer[::-1]:
            print("\n********************************************************************\n")
            for x in range(len(l)):
                line = '\t\t' + ' ' * x + ' \\'
                for y in l[x]:
                    line += (' \\ ' + y[0])
                print (line + ' \\ \\')
        print("\n********************************************************************")

    '''
    populates the ground level with all the ground types there are, in accordance to their proximity to water.
    It begins by finding a random location for the water, then populates the ground by going from the outer
    most layer to the inner most layer, then replacing the water at the end
    '''
    def fillGround(self):
        g = self.ground
        x, y = randint(0, len(g)-1), randint(0, len(g[0])-1)
        # go backwards through list of ground types and apply them to ground, layering down towards the goal center
        for type in self.groundTypes[::-1]:
            self.gFiller(x, y, type)
        # print ("Ground filled")

    '''
    creates a rectangle of (X1, Y1) to (X2, Y2) with a given radius from the water,
    resetting the coordinates to stay on the map
    '''
    def gFiller(self, x, y, type):
        radius = type[1]
        g = self.ground
        # set (X1, Y1). If either value goes negative, set it to 0 to stay on map
        X1, Y1 = x-radius, y-radius
        if X1 < 0: X1 = 0
        if Y1 < 0: Y1 = 0
        # set (X2, Y2). If either value goes beyond range of map, set it to edge to stay on map
        X2, Y2 = x + radius, y + radius
        if X2 > len(g[0])-1: X2 = len(g[0])-1
        if Y2 > len(g)-1: Y2 = len(g)-1
        # fill in the resulting square area with given type
        for i in range(1+X2 - X1):
            for j in range(1+Y2-Y1):
                g[i + X1][j + Y1] = type
                if type == self.groundTypes[0]: #if type == water, place on objects list
                    self.objects[0].update( {type : [(i + X1, j + Y1)]})

    '''
    Places 1 to 5 of each obstacle on the map, checking to not over ride where the water is.
    Starts on the ground altitude, then places the obstacles in the higher levels at the same (x, y)
    location depending on their height
    '''
    def fillObstacles(self):
        print ("filling obstacles")
        g = self.ground
        for obstacle in self.obstacles:
            numObstacles = randint(1, 5)
            for more in range(numObstacles):
                x, y = randint(0, len(g) - 1), randint(0, len(g[0]) - 1)
                # if (x, y) is water, get new (x, y)
                while (x, y) == self.objects[0].get(self.groundTypes[0])[0]:
                    x, y = randint(0, len(g) - 1), randint(0, len(g[0]) - 1)
                g[x][y] = obstacle
                # update both the layer the obstacle is in, as well as the
                for i in range(obstacle[1]):
                    self.layer[i][x][y] = (obstacle[0], )
                    self.objects[i].setdefault(obstacle, []).append((x, y))
        # test object for collision
        # self.layer[2][5][5] = 'Te', (5, 5)
        # self.objects[2].setdefault(('Te', 0), []).append((5, 5))

    '''
    Update map to keep a current tab of where the agent is as long as self.collision==False.
    Works for initial agent placement by including start==True to keep things simple for the agent
    '''
    def updateMap(self, agent, x, y, altitude, start=False):
        print "Environment: attempting update with", (x, y, altitude)
        if (x < 0) | (x > self.width) | (y < 0) | (y > self.height) | (altitude < 0) | (altitude > 2):
            print "Environment: placement is out of bounds", (x, y, altitude)
            return False
        if self.collision(x, y, altitude):
            print "Environment: Obstacle in the way at location", (x, y, altitude)
            return False
        if start == False:
            self.removeAgent(agent, x, y, altitude)
        self.addAgent(agent, x, y, altitude)
        print "Environment: drone update complete"

    '''
    Saves the info for the location the agent is moving to,
    then adds the agent with the saved data onto the map and self.objects[altitude] 
    '''
    def addAgent(self, agent, x, y, altitude):
        save = self.layer[altitude][y][x]
        self.layer[altitude][y][x] = (agent, save)
        self.objects[altitude].setdefault((agent, save), []).append((y, x))
        # print("Environment: successfully updated agent location")

    '''
    Remove Agent from map and returns the block where the agent was to the state it was before.
    i.e, if the block was a ('gr', 3) before the agent got there, the block becomes that again
    after the agent moves
    '''
    def removeAgent(self, agent, x, y, altitude):
        for l in self.objects:
            for m in l:
                if m[0] == agent:
                    keep = m[1]
                    keepX, keepY = l.get(m)[0]
                    self.layer[self.objects.index(l)][keepX][keepY] = keep
                    l.pop((m))
                    break

    '''
    Checks that the drone isn't trying to move somewhere where there's an existing obstacle
    '''
    def collision(self, x, y, altitude):
        for obj in self.objects[altitude]:
            for key in self.objects[altitude].get(obj):
                if (y, x) == key:
                    print "collision"
                    return True

    '''
    Returns the name of the item stored at the given coordinates, ignoring the agent's own location.
    A value of '__' means that that location is air/contains nothing
    '''
    def locationData(self, agent, x, y, altitude):
        if (x >= 0) & (y >= 0):
            if (x < self.width) & (y < self.height) & (altitude < 3): #<- hard coding in map height of 3. not sure how to get length of self.layer
                if self.layer[altitude][x][y][0] == agent:
                    return self.layer[altitude][x][y][1][0]
                return self.layer[altitude][x][y][0]
        return "over edge"


