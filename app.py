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

# redirect the base route to the calculator
@app.route('/')
def get_index():
    return redirect(url_for('get_calculator'))

# The route where the calculator app is located
@app.route('/BetweenTwoCitiesCalculator')
def get_calculator():
    return render_template('index.html')

# upload rout for images
# currently only saves the images in the uploads folder
# TODO: Pass the images into the image processor and get the score back
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        # TODO: flash error message
        return redirect(url_for('get_calculator'))

    # Get the file
    file = request.files['image']
    # Rename the file
    file.filename = f"file{len([f for f in os.listdir('uploads') if os.path.isfile(os.path.join('uploads', f))]) + 1}.jpg"

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        # TODO: Pass the image to the image processor to calculate score instead of saving it
        # then get back the score and pass it back to the front end
        file.save(file_path)  # Save the uploaded image to the uploads folder

        return redirect(url_for('get_calculator'))
