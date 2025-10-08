import cv2
import numpy as np

def stkimgs(scale, imgArray):
    # Get the number of rows in the input array
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]

    # If the input is a 2D array (grid of images)
    if rowsAvailable:
        # Loop through all rows and columns
        for x in range(rows):
            for y in range(cols):
                # If the current image dimensions match the first image, scale it
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    # Resize the current image to match the dimensions of the first image
                    imgArray[x][y] = cv2.resize(imgArray[x][y], 
                                                (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), 
                                                None, scale, scale)
                # Convert grayscale images to BGR format
                if len(imgArray[x][y].shape) == 2: 
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        
        # Create a blank image with the same dimensions as the first image
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        for x in range(rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                # Resize the current image to match the dimensions of the first image
                imgArray[x] = cv2.resize(imgArray[x], 
                                         (imgArray[0].shape[1], imgArray[0].shape[0]), 
                                         None, scale, scale)
            if len(imgArray[x].shape) == 2: 
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        
        # Horizontally stack all the images in the 1D array
        hor = np.hstack(imgArray)
        ver = hor

    return ver
