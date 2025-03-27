'''Test workspace to try and split a city image into tile images'''
import cv2
import os
import numpy as np
import imutils
from sklearn.cluster import DBSCAN
    


if __name__ == "__main__":
    # Load the image (provide the correct path)
    path = os.path.join(os.path.dirname(__file__), "images/city1.png")
    image = cv2.imread(path)
    image = imutils.resize(image, 500)
    #image = imutils.rotate(image, -10) # Test rotation

    #cv2.imshow("Image", image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("gray", gray)

    blur = cv2.GaussianBlur(gray, (51,51), 3)
    #cv2.imshow("blur", blur)

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
    #cv2.imshow("thresh", thresh)

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
    #cv2.imshow("Box", image)
    

    mask = np.zeros_like(gray)
    epsilon = 0.1*cv2.arcLength(city_countour, True)
    approx = cv2.approxPolyDP(city_countour, epsilon, True)
    cv2.drawContours(mask,[approx],0,255,-1)
    #cv2.imshow("mask", mask)

    masked = np.zeros_like(gray)
    masked[mask == 255] = blur[mask == 255]
    #cv2.imshow("Masked", masked)
    
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
    #cv2.imshow("Oriented", oriented)
    
    
    
    ###### Find tile centers ######
    tile_searches = {
        'tavern': [],
        'civic': [],
        'factory': [],
        'office': [],
        'shop': [],
        'park': []
    }
    tile_colors = {
        'tavern': (0, 0, 255),
        'civic': (255, 0, 128),
        'factory': (120, 120, 120),
        'office': (255, 0, 0),
        'shop': (0, 255, 255),
        'park': (0, 255, 0)
    }
    tile_thresholds = {
        'tavern': 0.80,
        'civic': 0.60,
        'factory': 0.80,
        'office': 0.80,
        'shop': 0.80,
        'park': 0.80
    }
    
    # Create found tiles image pyramid
    found_tiles = oriented.copy()
    tile_blur = ((5,5), 3)
    gray_found_tiles = cv2.cvtColor(found_tiles, cv2.COLOR_BGR2GRAY)
    found_tiles_pyramid = []
    for scale in np.linspace(.8, 1.2, 20)[::-1]:
        found_tiles_pyramid.append((scale, cv2.GaussianBlur(imutils.resize(gray_found_tiles, 
                                                                           int(gray_found_tiles.shape[0] * scale)),
                                                            ksize=tile_blur[0],
                                                            sigmaX=tile_blur[1])))
        
    # We know the tile is about 1/5 the width/height of the city
    tile_size = int((found_tiles.shape[0] + found_tiles.shape[1]) / 2 / 5)
    identified_tiles = []
    for tile_name in tile_searches.keys():
        template_path = os.path.join(os.path.dirname(__file__), 'images', 'tile_images', f'{tile_name}.png')
        template = cv2.imread(template_path)
        template = cv2.GaussianBlur(cv2.cvtColor(template, cv2.COLOR_BGR2GRAY), ksize=tile_blur[0], sigmaX=tile_blur[1])
        
        # The template has no border so it's 85% the size of a tile.
        template = imutils.resize(template, int(tile_size * 0.85)) # Just use the width for now. We don't want to distort the template.

        candidates = []
        for scale, level in found_tiles_pyramid:
            res = cv2.matchTemplate(level, template, cv2.TM_CCOEFF_NORMED)
            locs = np.where(res>=tile_thresholds[tile_name])
            locs = np.column_stack([locs[1], locs[0]])
            values = res[locs[:, 0], locs[:, 1]]
            locations = np.clip((locs / scale).astype(int), [0, 0], [found_tiles.shape[0] - 1, found_tiles.shape[1] - 1]) # After dividing, is coordiates at 1.0 scale
            candidates.extend(list(zip(locations.tolist(), values.tolist())))

        # Cluster
        clustered = DBSCAN(eps=tile_size/3).fit([c[0] for c in candidates])
        best_in_cluster = {}
        for cluster_label, c in zip(clustered.labels_, candidates):
            if cluster_label not in best_in_cluster:
                best_in_cluster[cluster_label] = c
            else:
                if best_in_cluster[cluster_label][1] < c[1]: # If we found one with higher score.
                    best_in_cluster[cluster_label] = c
            
        identified_tiles.extend([(loc, tile_name) for loc, _ in best_in_cluster.values()])

        # Draw some boxes
        boxes = []
        for location, value in best_in_cluster.values():
            boxes.append(np.array([location,
                                  [location[0], location[1] + template.shape[1]],
                                  [location[0] + template.shape[0], location[1] + template.shape[1]],
                                  [location[0] + template.shape[0], location[1]]]))
        
        found_tiles = cv2.drawContours(found_tiles, boxes, -1, tile_colors[tile_name])
        
    # Assemble grid
    # We do this by imposing a grid on the found tiles.
    # Step 1. Get bounding box of grid
    locations = np.asarray([loc for loc, _ in identified_tiles])
    min_x, min_y = np.min(locations, axis=0)
    max_x, max_y = np.max(locations, axis=0)
    
    # Step 2. Find the "indices" of each tile in this grid. (Grid isn't necessarily 5x5!)
    tile_indices = np.floor((locations - [min_x, min_y]) / tile_size).astype(int).tolist()
    
    # Step 3. Assemble a grid
    grid = {}
    for idx, tile_name in zip(map(tuple, tile_indices), [tile_name for _, tile_name in identified_tiles]):
        grid[idx] = tile_name
    print(grid)
    
    cv2.imshow("Tiles found", found_tiles)
    cv2.waitKey(0)
    
    

           
    