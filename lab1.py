import sys
from PIL import Image



def main():
    args = sys.argv[1:]

    # It should take 4 arguments, in order: 
    # terrain-image, elevation-file, path-file, output-image-filename

    terrainImage = args[0]
    elevationFile = args[1]
    pathFile = args[2]
    outputImageFilename = args[3]   

    # Program should return the total path length in meters to the terminal

    # Program should create a png image file of the  input map with the
    # optimal path drawn on top of it

    # - / - / - / - / - / - / - / FUNCTIONS / - / - / - / - / - / - / - /
    
    # function to create a pillow Image object from the image filename
    # returns a pillow image object
    image = createImage(terrainImage)

    # function to map terrain image file to a dictionary of pixels and
    # corresponding terrain difficulty. Returns a dictionary
    terrainMap = mapTerrain(image)

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
    pathLength = calulatePathLength(path)
    print(pathLength)

    # function which takes the orginial image and creates a new image
    # with the path drawn over top of it
    generateOutputImage(path, image, outputImageFilename)




if __name__ == '__main__':
    main()
