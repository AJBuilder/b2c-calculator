import os
import traceback
from flask import Flask, render_template, request, redirect, url_for, flash
from city_identification import CivicTileTypes, GenericCityTileTypes, TavernTileTypes, process_city_image

# Setup and Config
app = Flask(__name__, static_folder='static', template_folder='templates')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')  # Folder where images will be stored
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'fuzzylodgeawarddryergland'

# Ensure the upload directory exists
# TODO: NOT NECESSARY WHEN NOT SAVING IMAGES -> REMOVE WHEN READY
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Lookup to convert to what the Javascript is expecting
tile_lookup = {
    GenericCityTileTypes.Factory:           'factory',
    GenericCityTileTypes.Tavern:            'tavern',
    GenericCityTileTypes.Shop:              'shop',
    GenericCityTileTypes.Office:            'office',
    GenericCityTileTypes.Park:              'park',
    GenericCityTileTypes.House:             'house',
    GenericCityTileTypes.Civic:             'civic',
    GenericCityTileTypes.Landscape:         'empty',
    GenericCityTileTypes.HorizontalBridge:  'bridge horizontal',
    GenericCityTileTypes.VerticalBridge:    'bridge vertical',
    
    CivicTileTypes.Civic_Armory:            'civic factory civic park',
    CivicTileTypes.Civic_Bank:              'civic office factory tavern',
    CivicTileTypes.Civic_CarriageHouse:     'civic tavern shop office',
    CivicTileTypes.Civic_Cemetary:          'civic park civic shop',
    CivicTileTypes.Civic_CityHall:          'civic tavern civic factory',
    CivicTileTypes.Civic_College:           'civic office tavern civic',
    CivicTileTypes.Civic_Courthouse:        'civic office civic house',
    CivicTileTypes.Civic_ElementarySchool:  'civic house park tavern',
    CivicTileTypes.Civic_FireStation:       'civic house office civic',
    CivicTileTypes.Civic_HighSchool:        'civic shop park civic',
    CivicTileTypes.Civic_Hospital:          'civic tavern factory shop',
    CivicTileTypes.Civic_Library:           'civic office house shop',
    CivicTileTypes.Civic_MarketSquare:      'civic shop civic tavern',
    CivicTileTypes.Civic_MiddleSchool:      'civic shop house factory',
    CivicTileTypes.Civic_Monument:          'civic tavern park house',
    CivicTileTypes.Civic_Museum:            'civic office park factory',
    CivicTileTypes.Civic_PoliceStation:     'civic shop factory house',
    CivicTileTypes.Civic_PostOffice:        'civic house civic office',
    CivicTileTypes.Civic_SportsField:       'civic factory park office',
    CivicTileTypes.Civic_Treasury:          'civic office shop park',
    CivicTileTypes.Civic_WaterTower:        'civic tavern house park',
    
    TavernTileTypes.Tavern_Bed:             'tavern inn',
    TavernTileTypes.Tavern_Music:           'tavern music',
    TavernTileTypes.Tavern_Drink:           'tavern bar',
    TavernTileTypes.Tavern_Food:            'tavern restaurant',
    
    None:                                   'empty'
}


@app.route('/')
def get_index():
    return redirect(url_for('get_calculator')) # redirect the base route to the calculator


# The route where the calculator app is located
@app.route('/Calculator', methods = ("GET", "POST"))
def get_calculator():
    # Initial Default Values
    city_tiles: list[list[str]] = [
            ["empty", "empty", "empty", "empty", "empty"],
            ["empty", "empty", "empty", "empty", "empty"],
            ["empty", "empty", "empty", "empty", "empty"],
            ["empty", "empty", "empty", "empty", "empty"],
            ["empty", "empty", "empty", "empty", "empty"]
        ]
    if request.method == "GET":
        return render_template('index.html', city_tiles=city_tiles, scored=False)
    else:
        # Get the file
        file = request.files['image']
        
        if file.filename == '':
            # EITHER MANUAL SCORE WAS SELECTED OR SCORE CITY WAS SELECTED WITH NO IMAGE -> GIVE EMPTY CITY
            return render_template("index.html", city_tiles=city_tiles, scored=True)
        else:
            # Rename the file
            upload_dir = app.config['UPLOAD_FOLDER']
            file_count = len([f for f in os.listdir(upload_dir) if os.path.isfile(os.path.join(upload_dir, f))])
            file.filename = f"file{file_count + 1}.jpg"
            file_path = os.path.join(upload_dir, file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            try:
                for progress in process_city_image(file_path):
                    # TODO: Utilize "ratio" and "progress_str" fields for some kind of progress bar.
                    # Might need to run process_city_image in a seperate thread so this can return a page?
                    result = progress.get('result', None)
                    if result is not None:
                        for col_idx, col in enumerate(result):
                            for row_idx, tile in enumerate(col):
                                city_tiles[col_idx][row_idx] = tile_lookup.get(tile, 'error')
                        break # This break might not be necessary?
            except Exception as e:
                # TODO: do some better failure message
                print('Exception during process_city_image: \n' + traceback.format_exc())
            
            # Cleanup the file
            if os.path.exists(file_path):
                os.remove(file_path)

            print(city_tiles)
                
            return render_template("index.html", city_tiles=city_tiles, scored=True)