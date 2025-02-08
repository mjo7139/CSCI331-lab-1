import sys
from PIL import Image
import time
import matplotlib.pyplot as plt
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
    # Impassible vegetation	#054918 (5,73,24)           0
    (5, 73, 24):0,
    # Lake/Swamp/Marsh	        #0000FF (0,0,255)           2
    (0, 0, 255):2,
    # Paved road	            #473303 (71,51,3)           1
    (71, 51, 3):1,
    # Footpath	                #000000 (0,0,0)             1.1
    (0, 0, 0):1.1,
    # Out of bounds	        #CD0065 (205,0,101)	        0
    (205, 0, 101):0
    # - / - / - / - / - / - / - / - / - / - / - / - /
    }


    image = image.convert("RGB")
    im = image.load()
    image.save("debug_image.png")
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
    # Each pixel corresponds to an area of
    # 10.29 m in longitude (X) 
    # 7.55 m in latitude (Y)
    aX, aY = pixelA
    bX, bY = pixelB
    aZ = elevationMap[pixelA]
    bZ = elevationMap[pixelB]

    netX = (bX - aX) * 10.29
    netY = (bY - aY) * 7.55
    netZ = bZ - aZ

    sum1 = math.pow(netX, 2)
    sum2 = math.pow(netY, 2)
    sum3 = math.pow(netZ, 2)

    dist = math.sqrt(sum1 + sum2 + sum3)
    return dist

def generateF(pixelPos, pixelG, elevationMap, targetPos):
    # function generates an f value
    # -------------------- ISSUE FOR LATER ------------------
    # were going to run into problems because the get3dDist needs to be
    # the absolute value distance
    f = pixelG + get3Dist(targetPos, pixelPos, elevationMap)



def generateNeighbors(terrainMap, elevationMap, pos, target): 

    # this function  retuns a list of four tuples where the first element is 
    # the f value and the 2nd element is the pixel coordinates


def nextLeg(terrainMap, elevationMap, pos, target):
    # when thinking about the parent list and other things, i realized 
    # i would have a huge issue where heuristic values would be difficult
    # to overwrite. However I can solve many, many issues by limiting
    # the scope of everything from one point to another and simply repeating
    # this process

    # should return a deque of the final path taken from point A to point B
    path = deque()

    # !!!!!!!!!!!!!!!! TB DONE !!!!!!!!!!!!!!!!!
    # lets create a set of 4VAL tuples representing information for chekced pixels
    # the 4VAL tuple should include (position, parent, f value, g value)

    # our queue which is a heap of 2VAL tuples representing pixels where
    # (f value, position)
    prioQ = []

    while pos != target:
        # lets find each of the neighboring pixels and add them to a list to
        # be added to the heap, I need to make sure they arent on the heap though

        # retuns a list of tuples representing pixels (f value, position)
        toAdd = generateNeighbors(terrainMap, elevationMap, pos, target)
        for pixel in toAdd:
            if pixel not in parentDict:
                heapq.heappush(prioQ, pixel)
                parentDict.add((pixel[1], pos))
            elif pixel[0] < 

        # now that we have added all neighbors to the prioQ we are safe to change
        # our position to the next minnimum value node in the queue


def generatePath(terrainMap, elevationMap, destinations):

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
        route.appendleft(nextLeg(terrainMap, elevationMap, pos, target))
        # we must now continue the race from our new position which was our target
        pos = target




# - / - / - / - / - / - / - / calculatePathLength / - / - / - / - / - / - / - /

#def calculatePathLength(path): 
    # Each pixel corresponds to an area of
    # 10.29 m in longitude (X) 
    # 7.55 m in latitude (Y)

# - / - / - / - / - / - / - / generateOutputImage / - / - / - / - / - / - / - /

#def generateOutputImage(path, image, outputImageFilename): 
    # You should output an image of the input map with the optimal path
    #  drawn on top of it. This path should be 1 pixel wide and have the
    #  RGB value: #a146dd (161, 70, 221) 

# - / - / - / - / - / - / - / main / - / - / - / - / - / - / - /

def main():
    start = time.time()
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
    end = time.time()

    # function to map elevation points to a dictionary of pixels and
    # corresponding elevation. Returns a dictionary
    elevationMap = mapElevation(elevationFile)

    # function to generate a deque object of the locations to visit. 
    # returns a deque object
    route = generateRoute(pathFile) 

    # the main function which will generate the ideal path to follow using
    # a*. returns a deque object of the pixels visited, in order
    path = generatePath(terrainMap, elevationMap, route)

    # function to calculate the total path length to the terminal
    #pathLength = calulatePathLength(path)
    #print(pathLength)

    # function which takes the orginial image and creates a new image
    # with the path drawn over top of it
    #generateOutputImage(path, image, outputImageFilename)

    print(f"Time taken to run code was {end-start} seconds")




if __name__ == '__main__':
    main()
