import os
from flask import Flask, render_template, request, redirect, url_for, flash
from city_identification import CivicTileTypes, GenericCityTileTypes, TavernTileTypes, process_city_image

# Setup and Config
app = Flask(__name__)
# TODO: FOLDER TO SAVE IMAGES TO WILL NOT BE NEEDED IN THE FUTURE -> REMOVE WHEN READY
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder where images will be stored
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
    if request.method == "GET":
        # Initial Default Values
        city_tiles: list[list[str]] = [
            ["factory", "shop", "park", "tavern inn", "office"],
            ["factory", "shop", "park", "office","house"],
            ["factory", "shop", "empty", "empty", "house"],
            ["civc factory shop house", "shop", "empty", "empty", "bridge vertical"],
            ["tavern music", "office", "tavern food", "tavern bar", "civic tavern house factory"]
        ]
        return render_template('index.html', city_tiles=city_tiles, scored=False)
    else:
        # Get the file
        file = request.files['image']

        if not file.filename:
            # EITHER MANUAL SCORE WAS SELECTED OR SCORE CITY WAS SELECTED WITH NO IMAGE -> GIVE EMPTY CITY
            city_tiles: list[list[str]] = [
                ["empty", "empty", "empty", "empty", "empty"],
                ["empty", "empty", "empty", "empty", "empty"],
                ["empty", "empty", "empty", "empty", "empty"],
                ["empty", "empty", "empty", "empty", "empty"],
                ["empty", "empty", "empty", "empty", "empty"]
            ]
            # DUMMY CITY FOR TESTING -> REPLACE WITH EMPTY CITY
            # city_tiles: list[list[str]] = [
            #     ["factory", "shop", "park", "tavern inn", "office"],
            #     ["factory", "shop", "park", "office","house"],
            #     ["factory", "shop", "empty", "empty", "house"],
            #     ["civic factory shop house", "shop", "empty", "empty", "bridge vertical"],
            #     ["tavern music", "office", "tavern restaurant", "tavern bar", "civic tavern house factory"]
            # ]
            
            return render_template("index.html", city_tiles=city_tiles, scored=True)
        else:
            # Rename the file
            # TODO: REPLACE THIS WITH PASSING THE IMAGE TO THE PROCESSOR
            file.filename = f"file{len([f for f in os.listdir('uploads') if os.path.isfile(os.path.join('uploads', f))]) + 1}.jpg"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # TODO: REPLACE WITH PROCESSOR OUTPUT
            # TODO: DUMMY CITY FOR TESTING
            #city_tiles: list[list[str]] = [
            #    ["factory", "shop", "park", "tavern inn", "office"],
            #    ["factory", "shop", "park", "office","house"],
            #    ["factory", "shop", "empty", "empty", "house"],
            #    ["civic factory shop house", "shop", "empty", "empty", "bridge vertical"],
            #    ["tavern music", "office", "tavern restaurant", "tavern bar", "civic tavern house factory"]
            #]
            # city_tiles: list[list[str]] = [
            #     ["factory", "factory", "factory", "factory", "factory"],
            #     ["factory", "factory", "factory", "factory", "factory"],
            #     ["factory", "factory", "factory", "factory", "factory"],
            #     ["factory", "factory", "factory", "factory", "factory"],
            #     ["factory", "factory", "factory", "factory", "factory"]
            # ]
            
            
            city_tiles = process_city_image(file_path)
            
            for col_idx, col in enumerate(city_tiles):
                for row_idx, tile in enumerate(col):
                    city_tiles[col_idx][row_idx] = tile_lookup.get(tile, 'error')
            return render_template("index.html", city_tiles=city_tiles, scored=True)