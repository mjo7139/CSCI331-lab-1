import sys
from PIL import Image
import time

def mapTerrain(image):

def mapElevation(elevationFile): 
    # The elevation file corresponds to an area of 400x500 
    # (500 lines of 400 double values, each representing an 
    # elevation in meters). To address the difference in width 
    # between the elevation and terrain files you should just ignore
    # the last five values on each line of the elevation file.

def generateRoute(pathFile):
    # Terrain type	            Color on map	Photo (legend)
    # Open land	           #F89412 (248,148,18)	A
    # Rough meadow	           #FFC000 (255,192,0)	B
    # Easy movement forest	#FFFFFF (255,255,255)	C · D
    # Slow run forest	#02D03C (2,208,60)	E
    # Walk forest	#028828 (2,136,40)	F
    # Impassible vegetation	#054918 (5,73,24)	G
    # Lake/Swamp/Marsh	#0000FF (0,0,255)	H · I · J
    # Paved road	#473303 (71,51,3)	K · L
    # Footpath	#000000 (0,0,0)	M · N
    # Out of bounds	#CD0065 (205,0,101)	

def generatePath(terrainMap, elevationMap, route):
    # Each pixel corresponds to an area of
    # 10.29 m in longitude (X) 
    # 7.55 m in latitude (Y)

def calculatePathLength(path): 
    # Each pixel corresponds to an area of
    # 10.29 m in longitude (X) 
    # 7.55 m in latitude (Y)

def generateOutputImage(path, image, outputImageFilename): 
    # You should output an image of the input map with the optimal path
    #  drawn on top of it. This path should be 1 pixel wide and have the
    #  RGB value: #a146dd (161, 70, 221) 

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

    # - / - / - / - / - / - / - / FUNCTIONS / - / - / - / - / - / - / - /

    # function to map terrain image file to a dictionary of pixels and
    # corresponding terrain difficulty. Returns a dictionary
    terrainMap = mapTerrain(image)
    end = time.time()

    # function to map elevation points to a dictionary of pixels and
    # corresponding elevation. Returns a dictionary
    #elevationMap = mapElevation(elevationFile)

    # function to generate a deque object of the locations to visit. 
    # returns a deque object
    #route = generateRoute(pathFile) 

    # the main function which will generate the ideal path to follow using
    # a*. returns a deque object of the pixels visited, in order
    #path = generatePath(terrainMap, elevationMap, route)

    # function to calculate the total path length to the terminal
    #pathLength = calulatePathLength(path)
    #print(pathLength)

    # function which takes the orginial image and creates a new image
    # with the path drawn over top of it
    #generateOutputImage(path, image, outputImageFilename)

    print(f"Time taken to run code was {end-start} seconds")




if __name__ == '__main__':
    main()
