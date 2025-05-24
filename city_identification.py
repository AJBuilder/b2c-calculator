from enum import StrEnum, auto
import cv2
import os
import numpy as np
import imutils
from sklearn.cluster import DBSCAN
from itertools import repeat

class GenericCityTileTypes(StrEnum):
    Shop = auto()
    Factory = auto()
    Park = auto()
    Office = auto()
    Tavern = auto()
    Civic = auto()
    House = auto()
    VerticalBridge = auto()
    HorizontalBridge = auto()
    Landscape = auto()
    
class TavernTileTypes(StrEnum):
    Tavern_Bed = auto()
    Tavern_Food = auto()
    Tavern_Drink = auto()
    Tavern_Music = auto()

class CivicTileTypes(StrEnum):
    Civic_Armory = auto()
    Civic_Bank = auto()
    Civic_CarriageHouse = auto()
    Civic_Cemetary = auto()
    Civic_CityHall = auto()
    Civic_College = auto()
    Civic_Courthouse = auto()
    Civic_ElementarySchool = auto()
    Civic_FireStation = auto()
    Civic_HighSchool = auto()
    Civic_Hospital = auto()
    Civic_Library = auto()
    Civic_MarketSquare = auto()
    Civic_MiddleSchool = auto()
    Civic_Monument = auto()
    Civic_Museum = auto()
    Civic_PoliceStation = auto()
    Civic_PostOffice = auto()
    Civic_SportsField = auto()
    Civic_Treasury = auto()
    Civic_WaterTower = auto()


AllCityTileTypes = StrEnum('AllCityTileTypes', 
    {
        name: member.value
        for enum in (GenericCityTileTypes, TavernTileTypes, CivicTileTypes)
        for name, member in enum.__members__.items()
        if name not in {
            GenericCityTileTypes.Civic,
            GenericCityTileTypes.Tavern
        }
    })


def is_tavern(tile: str):
    return tile in TavernTileTypes or tile == GenericCityTileTypes.Tavern
        
def is_civic(tile: str):
    return tile in CivicTileTypes or tile == GenericCityTileTypes.Civic

def process_city_image(img_path: os.PathLike):
    '''Returns a 2D list where the index is the position with the top left being the origin and the contents being the tile string.'''
    # Load the image (provide the correct path)
    path = os.path.join(os.path.dirname(__file__), img_path)
    image = cv2.imread(path)
    small_image = imutils.resize(image, 500)
    #cv2.imshow("Image", image)
    
    
    ###### Outline/mask city ######
    # First step is to find the entire city grid as a whole.
    # We do this by finding the biggest contoured area and creating a mask for that area.
    # This is a KISS way of doing it, so might need to put in some other checks.

    gray = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)
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
                        
    rect = list(cv2.minAreaRect(city_countour))
    scalar = (image.shape[0] / small_image.shape[0], image.shape[1] / small_image.shape[1])
    rect[0] = np.multiply(rect[0], scalar)
    rect[1] = np.multiply(rect[1], scalar)
    box = cv2.boxPoints(rect)
    box = np.intp(box)
    #cv2.drawContours(image,[box],0,(0,0,255),2)
    #image = cv2.drawMarker(image, box[0],(0,0,255),2)
    #cv2.imshow("Box", image)

    #mask = np.zeros_like(gray)
    #epsilon = 0.1*cv2.arcLength(city_countour, True)
    #approx = cv2.approxPolyDP(city_countour, epsilon, True)
    #cv2.drawContours(mask,[approx],0,255,-1)
    #cv2.imshow("mask", mask)

    #masked = np.zeros_like(gray)
    #masked[mask == 255] = blur[mask == 255]
    #cv2.imshow("Masked", masked)
    
    
    
    ###### Orient city ######
    # We want to orient the city upright so that it's easier to work with.
    # (i.e. Up/down is Y, left/right is X.)
    # We do this by using a transformation matrix to warp the image.
    
    # Note: OpenCV pixel coordinates have the origin in the top left.
    
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
    
    # Create the matrix and multiply to warp.
    M = cv2.getPerspectiveTransform(start_pts, end_pts)
    oriented = cv2.warpPerspective(image, M, (width, height))
    #cv2.imshow("Oriented", oriented)
    
    # Resize
    oriented = imutils.resize(oriented, 500)
    
    ###### Find tiles ######
    # Now with the city identified and oriented, it's tile to identify the tiles.
    # We do this with template matching. Since the size of our template won't match
    # the size of the tile in the city exactly, we will do it multiple times with the city
    # scaled differently— forming an image pyramid.
    

    tile_colors = {
        GenericCityTileTypes.Tavern: (0, 0, 255),
        GenericCityTileTypes.Factory: (120, 120, 120),
        GenericCityTileTypes.Office: (255, 0, 0),
        GenericCityTileTypes.Shop: (0, 255, 255),
        GenericCityTileTypes.Park: (0, 255, 0),
        GenericCityTileTypes.House: (128, 128, 255)
    }
    tile_thresholds = {
        GenericCityTileTypes.Tavern: 0.8,
        GenericCityTileTypes.Factory: 0.8,
        GenericCityTileTypes.Office: 0.8,
        GenericCityTileTypes.Shop: 0.8,
        GenericCityTileTypes.Park: 0.8,
        GenericCityTileTypes.House: 0.8,
    }
    for c in CivicTileTypes:
        tile_colors[c] = (255, 0, 128)
        tile_thresholds[c] = 0.60
        
    first_pass = {
        GenericCityTileTypes.Tavern,
        GenericCityTileTypes.Factory,
        GenericCityTileTypes.Office,
        GenericCityTileTypes.Shop,
        GenericCityTileTypes.Park,
        GenericCityTileTypes.House,
        *set(CivicTileTypes)
    }
        
    
    # Create found tiles image pyramid
    found_tiles = oriented.copy()
    tile_blur = ((5,5), 3)
    gray_found_tiles = cv2.cvtColor(found_tiles, cv2.COLOR_BGR2GRAY)
    found_tiles_pyramid = []
    blurred_found_tiles_pyramid = []
    for scale in np.linspace(.8, 1.2, 20)[::-1]:
        found_tiles_pyramid.append((scale, imutils.resize(found_tiles, int(found_tiles.shape[0] * scale))))
        blurred_found_tiles_pyramid.append((scale, cv2.GaussianBlur(found_tiles_pyramid[-1][1],
                                                                    ksize=tile_blur[0],
                                                                    sigmaX=tile_blur[1])))
        
        
    # We know the tile is about 1/5 the width/height of the city
    tile_size = int((found_tiles.shape[0] + found_tiles.shape[1]) / 2 / 5)
    tile_candidates = []
    tile_template_size = int(tile_size * 0.85) # The template has no border so it's 85% the size of a tile.
    for tile_name in first_pass:
        if tile_name in CivicTileTypes:
            template_path = os.path.join(os.path.dirname(__file__), 'images', 'tile_images', 'civics', f'{tile_name}.png')
        else:
            template_path = os.path.join(os.path.dirname(__file__), 'images', 'tile_images', f'{tile_name}.png')
        template = cv2.imread(template_path)
        template = cv2.GaussianBlur(template, ksize=tile_blur[0], sigmaX=tile_blur[1])
        
        template = imutils.resize(template, tile_template_size) # Just use the width for now. We don't want to distort the template.

        for scale, level in blurred_found_tiles_pyramid:
            res = cv2.matchTemplate(level, template, cv2.TM_CCOEFF_NORMED)
            locs = np.where(res>=tile_thresholds[tile_name])
            locs = np.column_stack([locs[1], locs[0]])
            values = res[np.clip(locs[:, 0], 0, a_max=res.shape[0] - 1), np.clip(locs[:, 1], 0, a_max=res.shape[1] - 1)]
            # After dividing, is coordiates at 1.0 scale. Add half the size to convert to tile center.
            locations = np.clip(((locs / scale) + (tile_template_size / 2)).astype(int), [0, 0], [found_tiles.shape[0] - 1, found_tiles.shape[1] - 1])
            tile_candidates.extend(list(zip(locations.tolist(), values.tolist(), repeat(tile_name))))


    
    ###### Match landscape ######
    # The landscapes are 3x3, so they are 3/5 the size of the city.
    landscape_size = int((found_tiles.shape[0] + found_tiles.shape[1]) / 2 * 3 / 5)
    # A mapping of the relative position of each "tile" of a landscape to the top-left origin.
    landscape_tiles = {
        'canyon': {
            GenericCityTileTypes.Landscape: [(1,0), (1,2), (0,2), (2,2)],
            GenericCityTileTypes.HorizontalBridge: [(1,1)]
        },
        'flowers': {
            GenericCityTileTypes.Landscape: [(1,0), (2,0), (1,2), (2,2)],
            GenericCityTileTypes.HorizontalBridge: [(1,1)]
        },
        'island': {
            GenericCityTileTypes.Landscape: [(1,0), (1,1)],
            GenericCityTileTypes.HorizontalBridge: [(1,2)],
            GenericCityTileTypes.VerticalBridge: [(0,1), (2,1)]
        },
        'lake': {
            GenericCityTileTypes.Landscape: [(2,0), (1,1), (2,1)],
            GenericCityTileTypes.HorizontalBridge: [(1,2)],
            GenericCityTileTypes.VerticalBridge: [(0,1)]
        },
        'marsh': {
            GenericCityTileTypes.Landscape: [(1,0), (2,0), (0,2), (1,2)],
            GenericCityTileTypes.HorizontalBridge: [(1,1)]
        },
        'mountains': {
            GenericCityTileTypes.Landscape: [(2,0), (2,1), (0,2), (2,2)],
            GenericCityTileTypes.VerticalBridge: [(1,1)]
        },
        'waterfall': {
            GenericCityTileTypes.Landscape: [(0,0), (1,0), (0,1), (1,1)],
            GenericCityTileTypes.VerticalBridge: [(2,1)]
        },
    }
    identified_landscape = None
    for land_name, land_tiles in landscape_tiles.items():
        # Load template image with alpha channel
        template_path = os.path.join(os.path.dirname(__file__), 'images', 'landscapes', f'{land_name}.png')
        template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
        template = imutils.resize(template, landscape_size) # Just use the width for now. We don't want to distort the template.

        # Split channels
        alpha_channel = template[:, :, 3]   # Extract alpha channel
        template = template[:, :, :3]  # Extract BGR channels
        #template = cv2.GaussianBlur(cv2.cvtColor(bgr_template, cv2.COLOR_BGR2GRAY), ksize=tile_blur[0], sigmaX=tile_blur[1])

        # Create a mask from the alpha channel (non-zero means consider in matching)
        mask = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)[1]

        # Perform template matching using the mask
        result = cv2.matchTemplate(found_tiles, template, cv2.TM_CCOEFF_NORMED, mask=mask)

        # Get the best match location
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
        if max_val > 0.4:
            identified_landscape = land_name
            found_tiles = cv2.drawMarker(found_tiles, max_loc, (255,255,0))
            for name, locations in land_tiles.items():
                # Using the relative positions of each tile in relation to the landscape origin,
                # find the center of each landscape tile.
                tile_candidates.extend([((int(((relative_loc[0] * tile_size) + (tile_size / 2)) + max_loc[0]), int((relative_loc[1] * tile_size) + (tile_size / 2)) + max_loc[1]), max_val, name) for relative_loc in locations])
            break
        
    
    # Cluster
    clustered = DBSCAN(eps=tile_size/3, min_samples=1).fit([loc for loc, _, _ in tile_candidates])
    best_in_cluster = {}
    for cluster_label, c in zip(clustered.labels_, tile_candidates):
        if cluster_label not in best_in_cluster:
            best_in_cluster[cluster_label] = c
        else:
            if best_in_cluster[cluster_label][1] < c[1]: # If we found one with higher score.
                best_in_cluster[cluster_label] = c
    identified_tiles = [(loc, name) for loc, _, name in best_in_cluster.values()]
        
    ###### Draw some boxes ######
    for location, name in identified_tiles:
        half_tile_template_size = int(tile_template_size / 2)
        box = np.array([[location[0] - half_tile_template_size, location[1] - half_tile_template_size],
                        [location[0] - half_tile_template_size, location[1] + half_tile_template_size],
                        [location[0] + half_tile_template_size, location[1] + half_tile_template_size],
                        [location[0] + half_tile_template_size, location[1] - half_tile_template_size]])
        found_tiles = cv2.drawContours(found_tiles, [box], -1, tile_colors[name] if name in tile_colors else (255,255,255))
    
        
    ###### Assemble grid ######
    # We do this by imposing a grid on the found tiles.
    # Step 1. Get origin of the grid.
    locations = np.asarray([loc for loc, _ in identified_tiles])
    grid_origin = np.min(locations, axis=0) - int(tile_size / 2)
    
    # Step 2. Find the "indices" of each tile in this grid. (Grid isn't necessarily 5x5!)
    # i.e. How many multiples of the tile size the location is away from the grid origin.
    tile_indices = np.floor((locations - grid_origin) / tile_size).astype(int).tolist()
    
    # Step 3. Assemble a grid
    grid = {}
    for idx, tile_name in zip(map(tuple, tile_indices), [tile_name for _, tile_name in identified_tiles]):
        grid[idx] = tile_name
    
    
    ##### Identify specific tavern ####
    for loc, name in grid.items():
        if name != 'tavern':
            continue
        
        tile_pyramid = []
        for scale, image in found_tiles_pyramid:
            scaled_tile_size = int(tile_size * scale)
            scaled_tile_size_half = int(scaled_tile_size / 2)
            scaled_loc = (int(loc[0] * scaled_tile_size + scaled_tile_size_half), int(loc[1] * scaled_tile_size + scaled_tile_size_half))
            tile = image[max(0, scaled_loc[1] - scaled_tile_size_half) : min(image.shape[1], scaled_loc[1] + scaled_tile_size_half),
                         max(0, scaled_loc[0] - scaled_tile_size_half) : min(image.shape[0], scaled_loc[0] + scaled_tile_size_half)]
            tile_pyramid.append((scale, tile))
            
        type_results = {}
        crop_start = int(tile_template_size * .09)
        crop_end = int(crop_start + tile_template_size*.25)
        for tavern_type in TavernTileTypes:
            template_path = os.path.join(os.path.dirname(__file__), 'images', 'tile_images', 'taverns', f'{tavern_type}.png')
            template = cv2.imread(template_path)
            template = imutils.resize(template, tile_template_size)
            template = template[crop_start : crop_end, crop_start : crop_end]
            best = 0
            for scale, image in tile_pyramid:
                res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)
                if max_val > best:
                    best = max_val
            type_results[tavern_type] = best
        best_type = max(type_results, key=type_results.get)
        grid[loc] = best_type
                
            
    cv2.imshow("Tiles found", found_tiles)
    print(grid)
    
    list_grid = []
    def set_2d(matrix, row, col, value):
        # Ensure the outer list has enough rows
        while len(matrix) <= row:
            matrix.append([])

        # Ensure the specific row has enough columns
        while len(matrix[row]) <= col:
            matrix[row].append(None)  # Use any default filler value you want

        # Set the value
        matrix[row][col] = value
    for (x, y), tile in grid.items():
        set_2d(list_grid, y, x, tile) # Janky flip since the Javascript interprets it flipped?
        
    
    #print(list_grid)
    return list_grid
    
    
#process_city_image(r'images\city1.png')
#process_city_image(r'uploads\file21.jpg')
#cv2.waitKey()