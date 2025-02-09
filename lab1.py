import sys
from PIL import Image
#import time
from collections import deque
import heapq
import math

# - / - / - / - / - / - / - / mapTerrain / - / - / - / - / - / - / - /

def mapTerrain(image):
    terrain__costs = {
    # Terrain type	             Color on map                Movecost
    # Open land	            #F89412 (248,148,18)        1.15
    (248, 148, 18):1.15,
    # Rough meadow	            #FFC000 (255,192,0)	        1.3
    (255, 192, 0):1.3,
    # Easy movement forest     #FFFFFF (255,255,255)       1.2
    (255, 255, 255):1.2,
    # Slow run forest	        #02D03C (2,208,60)          1.25
    (2, 208, 60):1.25,
    # Walk forest	            #028828 (2,136,40)          1.6
    (2, 136, 40):1.6,
    # Impassible vegetation	#054918 (5,73,24)           999
    (5, 73, 24):999,
    # Lake/Swamp/Marsh	        #0000FF (0,0,255)           2
    (0, 0, 255):2,
    # Paved road	            #473303 (71,51,3)           1
    (71, 51, 3):1,
    # Footpath	                #000000 (0,0,0)             1.1
    (0, 0, 0):1.1,
    # Out of bounds	        #CD0065 (205,0,101)	        999
    (205, 0, 101):999
    # - / - / - / - / - / - / - / - / - / - / - / - /
    }


    image = image.convert("RGB")
    im = image.load()
    #image.save("debug_image.png")
    dict = {}
    tempCost = None
    tempColor = None
    for x in range(image.width):
        for y in range(image.height): 
            tempColor = im[x, y]
            tempCost = terrain__costs.get(tempColor, None)
        
            if tempCost is None:
                print(image.mode)
                print(f"Matt's ERROR: Unrecognized terrain color {tempColor} at {x, y}")
                return

            dict[(x, y)] = tempCost

    return dict

# - / - / - / - / - / - / - / mapElevation / - / - / - / - / - / - / - /

def mapElevation(elevationFile): 
    # The elevation file corresponds to an area of 400x500 
    # (500 lines of 400 double values, each representing an 
    # elevation in meters). To address the difference in width 
    # between the elevation and terrain files you should just ignore
    # the last five values on each line of the elevation file.

    x = 0
    y = 0
    dict = {}

    with open(elevationFile, "r") as file:
        lines = file.readlines()
        for line in lines:
            words = line.strip().split()
            for word in words:
                if x < 395:
                    tempList = word.split("e")
                    word = tempList[0]
                    # WARNING: We are hard coding the times 100 which is 
                    # converting scientific notation to normal
                    dict[(x, y)] = float(word) * 100
                    x += 1
            x = 0
            y += 1
    return dict
                


# - / - / - / - / - / - / - / generateRoute / - / - / - / - / - / - / - /

def generateRoute(pathFile):
    #deque object to be returned
    queue = deque()
    with open(pathFile, "r") as file:
        lines = file.readlines()
        for line in lines:
            line.strip()
            # a deque is defaulted to popping off of the right side
            # and so we want to append to the left side each time so that
            # the first line / coordinate appended ends up at the right 
            # side at the end
            temp = line.split()
            x = int(temp[0])
            y = int(temp[1])
            queue.appendleft((x, y))

    return queue



# - / - / - / - / - / - / - / generatePath / - / - / - / - / - / - / - /

def get3Dist(pixelA, pixelB, elevationMap):
    # ! CHECK !
    # Each pixel corresponds to an area of
    # 10.29 m in longitude (X) 
    # 7.55 m in latitude (Y)
    aX, aY = pixelA
    bX, bY = pixelB
    aZ = elevationMap[pixelA]
    bZ = elevationMap[pixelB]

    netX = abs(bX - aX) * 10.29
    netY = abs(bY - aY) * 7.55
    netZ = abs(bZ - aZ)

    sum1 = math.pow(netX, 2)
    sum2 = math.pow(netY, 2)
    sum3 = math.pow(netZ, 2)

    dist = math.sqrt(sum1 + sum2 + sum3)
    return dist

def retrace(state): 
    #                                    [0]       [1]      [2]    [3]     [4]     [5]
    # a tuple representing our state (curPixel, targetPos, check, posQ, tupleSet, path)
    
    curPix = state[0]
    parentPix = curPix[1]
    # add the final location to the path, this will be the last location 
    # popped from the path later
    state[5].append(curPix[0])
    
    while parentPix is not None:
        # now lets add the parent location
        state[5].append(parentPix[0])
        # set the parent to the parent of the one we just added
        parentPix = parentPix[1]
        # we continue this until we get back to the start which has a parent of none

    # returns the state
    return state


def newPoint(terrainMap, elevationMap, state, newPointPos): 
    #                                    [0]       [1]      [2]    [3]     [4]     [5]
    # a tuple representing our state (curPixel, targetPos, check, posQ, tupleSet, path)

    #                                 [0]       [1]     [2]     [3]
    # a tuple representing pixels (position, parent, g value, h value)
    newPoint = (
        newPointPos, 
        state[0], 
        (state[0][2]) + (terrainMap[newPointPos] * get3Dist(state[0][0], newPointPos, elevationMap)), 
        get3Dist(newPointPos, state[1], elevationMap))


    heapq.heappush(state[3], ( (newPoint[2]+newPoint[3]), (newPointPos)))
    #state[4].add(newPoint)
    state[4][newPoint[0]] = newPoint
    state[2].add(newPointPos)
    return state


def checkReplicte(state, neighborPos, elevationMap, terrainMap): 
    #                                    [0]       [1]      [2]    [3]     [4]     [5]
    # a tuple representing our state (curPixel, targetPos, check, posQ, tupleSet, path)

    # returns a tuple of state
    #for pixel in state[4]:
    #    if pixel[0] == neighborPos:
    pixel = state[4][neighborPos]
    newG = (state[0][2]) + (terrainMap[neighborPos] * get3Dist(state[0][0], neighborPos, elevationMap))
    newH = get3Dist(neighborPos, state[1], elevationMap)
    newF = newG + newH
    if (pixel[2]+pixel[3]) > newF: 
        #state[4].remove(pixel)
        #state[4].add((neighborPos, state[0], newG, newH))
        state[4][neighborPos] = (neighborPos, state[0], newG, newH)
        state[3].remove((pixel[2]+pixel[3], pixel[0]))
        state[3].append((newF, neighborPos))
        heapq.heapify(state[3])
        return state
    else:
        return state
            

    print("Matt Error: LOOKING FOR NONEXISTANT PIXEL")
    return state

def considerNeighbor(terrainMap, elevationMap, state, neighborPos):
    #                                    [0]       [1]      [2]    [3]     [4]     [5]
    # a tuple representing our state (curPixel, targetPos, check, posQ, tupleSet, path)

    # we should only be adding to the posQ in this function and below

    # is the neighbor a valid location?
    if neighborPos[0] < 0 or neighborPos[0] >= 395:
        return state
    if neighborPos[1] < 0 or neighborPos[1] >= 500:
        return state
    # is the neighbor even passible?
    if terrainMap[neighborPos] >= 998:
        return state
    # have we checked this point already?
    if neighborPos in state[2]:
        # ok it has been checked. switch our the old with the new replicate 
        # if the new f value is lower than the old ones
        state = checkReplicte(state, neighborPos, elevationMap, terrainMap)
        return state
    
    # else we have a new point which is at a valid location and is passible and is not a replicate
    state = newPoint(terrainMap, elevationMap, state, neighborPos)
    return state


    
            
def step1(terrainMap, elevationMap, state):
    #                                    [0]       [1]      [2]    [3]     [4]     [5]
    # a tuple representing our state (curPixel, targetPos, check, posQ, tupleSet, path)

    curPixel = state[0]
    curPos = curPixel[0]
    

    north = curPos
    north = (north[0] - 1, north[1])
    state = considerNeighbor(terrainMap, elevationMap, state, north)
    
    east = curPos
    east = (east[0], east[1] + 1)
    state = considerNeighbor(terrainMap, elevationMap, state, east)

    south = curPos
    south = (south[0] + 1, south[1])
    state = considerNeighbor(terrainMap, elevationMap, state, south)

    west = curPos
    west = (west[0], west[1] - 1)
    state = considerNeighbor(terrainMap, elevationMap, state, west)

    
    return state

def step2(state):
    #                                    [0]       [1]      [2]    [3]     [4]     [5]
    # a tuple representing our state (curPixel, targetPos, check, posQ, tupleSet, path)
    nextUp = heapq.heappop(state[3])
    #print(nextUp)

    # find the next pixel in the tupleset
    # -------- TO BE OPTIMIZED --------------
    # yes i know iterating over a set is slow but were gonna deal with it for now
    #for pixel in state[4]:
    #    if pixel[0] == nextUp[1]:
    #        state[0] = pixel
    #        return state

    state[0] = state[4][nextUp[1]]
    return state
    #print("Matt's Error: couldnt find next stepping pixel")
    #return

def nextLeg(terrainMap, elevationMap, pos, target):
    # should return a deque of the final path taken from point A to point B
    path = deque()
    # a set of positions representing pixels (position)
    check = set()
    #                                         [0]       [1]     [2]     [3]
    # a set of tuples representing pixels (position, parent, g value, h value)
    tupleSet = dict()
    #                                         [0]       [1]   
    # a heap of tuples representing pixels (f value, position)
    posQ = []

    # lets add the starting location to our structures
    check.add(pos)
    curPixel = (pos, None, 0, get3Dist(pos, target, elevationMap))
    tupleSet[curPixel[0]] = curPixel

    #                                    [0]       [1]      [2]    [3]     [4]     [5]
    # a tuple representing our state (curPixel, targetPos, check, posQ, tupleSet, path)
    # changed (...) to [...]
    state = [curPixel, target, check, posQ, tupleSet, path]

   

    while state[0][0] != state[1]:
        # step1 add's all of the new ,neighbors to the queue
        #print("curloc + " + str(state[0][0]))
        #print("targetloc + " + str(state[1][0]))
        state = step1(terrainMap, elevationMap, state)

        state = step2(state)
        

        # debugging: print the step each step
        #print(state[0])

    # retrace the path we took
    state = retrace(state)

    # return the path
    return state[5]


def generatePath(terrainMap, elevationMap, destinations):
    # ! CHECK !
    # Ok, we have a list of locations to visit on out "destinations" including a 
    # starting point and an ending point. First lets record our current position
    # i.e. the first point on our route
    
    pos = destinations.pop()

    # lets create a deque object to keep track of the routes taken, this should only
    # be updated once we reach a destination
    route = deque()

    
    while len(destinations) >= 1:
        target = destinations.pop()
        
        # find the optimal path for this leg and add it to the route
        route.append(nextLeg(terrainMap, elevationMap, pos, target))
        # we must now continue the race from our new position which was our target
        pos = target
    return route

# - / - / - / - / - / - / - / generateOutputImage / - / - / - / - / - / - / - /

def drawPoints(destinations, newImage):
    while len(destinations) > 0:
        draw = destinations.pop()
        newImage.putpixel(draw, (255, 0, 0))
    return newImage


def generateOutputImage(path, image, outputImageFilename, destinations, elevationMap): 
    # You should output an image of the input map with the optimal path
    #  drawn on top of it. This path should be 1 pixel wide and have the
    #  RGB value: #a146dd (161, 70, 221) 

    newImage = image.copy()
    total = 0

    # path is a deque of deque objects
    # popping from the top will give us our first leg
    
    while len(path) > 0:
        leg = path.pop()
        draw = leg.pop()
        newImage.putpixel(draw, (161, 70, 221))

        a = draw

        draw = leg.pop()
        newImage.putpixel(draw, (161, 70, 221))

        b = draw
        total += get3Dist(a, b, elevationMap)
        while len(leg) > 0:
            draw = leg.pop()
            newImage.putpixel(draw, (161, 70, 221))
            a = b
            b = draw
            total += get3Dist(a, b, elevationMap)

        
    # this is entirely for debugging purposes
    #newImage = drawPoints(destinations, newImage)

    newImage.save(outputImageFilename, "PNG")
    return total

# - / - / - / - / - / - / - / main / - / - / - / - / - / - / - /

def main():
    #start = time.time()
    args = sys.argv[1:]


    # It should take 4 arguments, in order: 
    # terrain-image, elevation-file, path-file, output-image-filename

    terrainImage = args[0]
    elevationFile = args[1]
    pathFile = args[2]
    outputImageFilename = args[3]  

    
    image = Image.open(terrainImage)

    # Program should return the total path length in meters to the terminal

    # Program should create a png image file of the  input map with the
    # optimal path drawn on top of it

    # -------------------- FUNCTIONS ----------------

    # function to map terrain image file to a dictionary of pixels and
    # corresponding terrain difficulty. Returns a dictionary
    terrainMap = mapTerrain(image)
    #end = time.time()

    # function to map elevation points to a dictionary of pixels and
    # corresponding elevation. Returns a dictionary
    elevationMap = mapElevation(elevationFile)

    # function to generate a deque object of the locations to visit. 
    # returns a deque object
    route = generateRoute(pathFile) 
    route2 = route.copy()

    # the main function which will generate the ideal path to follow using
    # a*. returns a deque object of the pixels visited, in order
    path = generatePath(terrainMap, elevationMap, route)
    path2 = path.copy()

    # function to calculate the total path length to the terminal and which 
    # takes the orginial image and creates a new image with the path drawn over top of it
    pathLength = generateOutputImage(path2, image, outputImageFilename, route2, elevationMap)
    print(str(pathLength))

    #print(f"Time taken to run code was {end-start} seconds")




if __name__ == '__main__':
    main()
