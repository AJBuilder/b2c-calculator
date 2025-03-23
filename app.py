import os
from flask import Flask, render_template, request, redirect, url_for, flash

# Setup and Config
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder where images will be stored
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'fuzzylodgeawarddryergland'
# Ensure the upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


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

        if file.filename == '':
            # TODO: this means manual score has been selected so pass an empty city to the template
            print('NO FILE') # Don't save a file that doesn't exist
            city_tiles: list[list[str]] = [
                ["factory", "shop", "park", "tavern inn", "office"],
                ["factory", "shop", "park", "office","house"],
                ["factory", "shop", "empty", "empty", "house"],
                ["civic factory shop house", "shop", "empty", "empty", "bridge vertical"],
                ["tavern music", "office", "tavern restaurant", "tavern bar", "civic tavern house factory"]
            ]
            return render_template("index.html", city_tiles=city_tiles, scored=True)
        else:
            # Rename the file
            # TODO: REPLACE THIS WITH PASSING THE IMAGE TO THE PROCESSOR
            file.filename = f"file{len([f for f in os.listdir('uploads') if os.path.isfile(os.path.join('uploads', f))]) + 1}.jpg"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # TODO: REPLACE WITH PROCESSOR OUTPUT
            city_tiles: list[list[str]] = [
                ["factory", "shop", "park", "tavern inn", "office"],
                ["factory", "shop", "park", "office","house"],
                ["factory", "shop", "empty", "empty", "house"],
                ["civic factory shop house", "shop", "empty", "empty", "bridge vertical"],
                ["tavern music", "office", "tavern restaurant", "tavern bar", "civic tavern house factory"]
            ]
            # city_tiles: list[list[str]] = [
            #     ["factory", "factory", "factory", "factory", "factory"],
            #     ["factory", "factory", "factory", "factory", "factory"],
            #     ["factory", "factory", "factory", "factory", "factory"],
            #     ["factory", "factory", "factory", "factory", "factory"],
            #     ["factory", "factory", "factory", "factory", "factory"]
            # ]
            return render_template("index.html", city_tiles=city_tiles, scored=True)