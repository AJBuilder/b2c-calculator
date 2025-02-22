'''Test workspace to try and split a city image into tile images'''
import cv2
import os
import numpy as np
import imutils
import time
    


if __name__ == "__main__":
    # Load the image (provide the correct path)
    path = os.path.join(os.path.dirname(__file__), "images/city1.png")
    image = cv2.imread(path)
    image = imutils.resize(image, 500)
    #image = imutils.rotate(image, -10) # Test rotation

    cv2.imshow("Image", image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray", gray)

    blur = cv2.GaussianBlur(gray, (51,51), 3)
    cv2.imshow("blur", blur)

    #thresh = None
    #def update(val):
    #    block_size = cv2.getTrackbarPos('block_size', 'trackbars') * 2 + 1
    #    C = (cv2.getTrackbarPos('C', 'trackbars') / 2)
    #    print(f'block_size: {block_size}, C: {C}')
    #    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, C)
    #    cv2.imshow("thresh", thresh)
        
    #cv2.namedWindow('trackbars')
    #cv2.createTrackbar('block_size', 'trackbars', 11, 100, update)
    #cv2.createTrackbar('C', 'trackbars', 11, 20, update)
    #update(0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 23, 0)
    cv2.imshow("thresh", thresh)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    max_area = 0
    city_countour = None
    areas = []
    
    # Find the biggest contour.
    for cont in contours:
            area = cv2.contourArea(cont)
            areas.append(area)
            if area > 1000:
                    if area > max_area:
                        max_area = area
                        city_countour = cont
                        
    rect = cv2.minAreaRect(city_countour)
    box = cv2.boxPoints(rect)
    box = np.intp(box)
    cv2.drawContours(image,[box],0,(0,0,255),2)
    image = cv2.drawMarker(image,box[0],(0,0,255),2)
    cv2.imshow("Box", image)
    

    mask = np.zeros_like(gray)
    epsilon = 0.1*cv2.arcLength(city_countour, True)
    approx = cv2.approxPolyDP(city_countour, epsilon, True)
    cv2.drawContours(mask,[approx],0,255,-1)
    cv2.imshow("mask", mask)

    masked = np.zeros_like(gray)
    masked[mask == 255] = blur[mask == 255]
    cv2.imshow("Masked", masked)
    
    ###### Orient city ######
    # We do this by using a transformation matrix to warp the image.
    
    # If the angle is more than 45, than shift the first point to the end.
    # The start of the box is in the bottom left, if it is more than 45deg rotate,
    # than the start would be in the top left of the image.
    if rect[2] > 45:
        box = np.roll(box, 1, 0)
        
    # Extract the width and height
    width = int(rect[1][0])
    height = int(rect[1][1])
        
    start_pts = box.astype("float32") # Starting points
    end_pts = np.array([[0, height-1], # Target end location of start points
                        [0, 0],
                        [width-1, 0],
                        [width-1, height-1]], dtype="float32")
    
    # Create the matrix
    M = cv2.getPerspectiveTransform(start_pts, end_pts)
    oriented = cv2.warpPerspective(image, M, (width, height))
    cv2.imshow("Oriented", oriented)
    
    
    
    ###### Find tile centers ######
    # For now, let's just divide the image into 25 tiles.
    tile_width = int(width / 5)
    tile_height = int(height / 5)
    tile_images = []
    for r in range(0, 5):
        row = []
        for c in range(0,5):
            row.append(oriented[tile_width * c:tile_width * (c+1), tile_height * r:tile_height * (r+1)] )
            #cv2.imshow(f"Tile_{r}-{c}", row[-1])
        tile_images.append(row)
            
    def classify_tile(tile_image):
        
        # Get top left symbol. (Top left 1/3)
        symbol = tile_image[int(tile_width/10):int(tile_width/2), int(tile_height/10):int(tile_height/2)]
        
        # Find max color
        symbol_hsv = cv2.cvtColor(symbol, cv2.COLOR_BGR2HSV)
        cv2.namedWindow('Trackbars')
        def update(_):
            h_min = cv2.getTrackbarPos('Hue Min', 'Trackbars')
            h_max = cv2.getTrackbarPos('Hue Max', 'Trackbars')
            s_min = cv2.getTrackbarPos('Sat Min', 'Trackbars')
            s_max = cv2.getTrackbarPos('Sat Max', 'Trackbars')
            v_min = cv2.getTrackbarPos('Val Max', 'Trackbars')
            v_max = cv2.getTrackbarPos('Val Min', 'Trackbars')
            lower = np.array([h_min, s_min, v_min])
            upper = np.array([h_max, s_max, v_max])
            filtered_symbol = cv2.inRange(symbol_hsv, lower, upper)
            cv2.imshow("Filtered Symbol", filtered_symbol)
        cv2.createTrackbar('Hue Min', 'Trackbars', 0, 255, update)
        cv2.createTrackbar('Hue Max', 'Trackbars', 0, 255, update)
        cv2.createTrackbar('Sat Min', 'Trackbars', 0, 255, update)
        cv2.createTrackbar('Sat Max', 'Trackbars', 0, 255, update)
        cv2.createTrackbar('Val Max', 'Trackbars', 0, 255, update)
        cv2.createTrackbar('Val Min', 'Trackbars', 0, 255, update)
        cv2.waitKey(0)
        
            
    for row in tile_images:
        for tile in row:
            classify_tile(tile)

           
    