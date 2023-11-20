from flask import Flask, flash, redirect, request, render_template, redirect, url_for
import tensorflow as tf 
import numpy as np
from PIL import Image
import os
from werkzeug.utils import secure_filename
import pandas as pd


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/portfolio-details')
def portfolio_details():
    return render_template('portfolio-details.html')


@app.route('/action')
def action():
    return render_template('action.html')


UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


model = tf.keras.models.load_model("D:\Learnings\LeafLife\Final_Model.h5")
disease_info = pd.read_csv('disease_info.csv', encoding='cp1252')


class_mapping = {0: 'Apple : Apple Scab',
                 1: 'Apple : Black Rot',
                 2: 'Apple : Cedar Apple Rust',
                 3: 'Apple : Healthy',
                 4: 'Cherry : Powdery Mildew',
                 5: 'Cherry : Healthy',
                 6: 'Corn : Cercospora Leaf Spot | Gray leaf spot',
                 7: 'Corn : Common Rust',
                 8: 'Corn : Northern Leaf Blight',
                 9: 'Grape : Black Rot',
                 10: 'Grape : Esca (Black_Measles)',
                 11: 'Grape : Leaf blight (Isariopsis_Leaf_Spot)',
                 12: 'Grape : healthy',
                 13: 'Orange : Haunglongbing (Citrus Greening)',
                 14: 'Orange : Black Spot',
                 15: 'Orange : Citrus Canker',
                 16: 'Peach : Bacterial Spot',
                 17: 'Peach : Healthy',
                 18: 'Pepper bell : Bacterial Spot',
                 19: 'Pepper bell : Healthy',
                 20: 'Potato : Early Blight',
                 21: 'Potato : Late Blight',
                 22: 'Potato : Healthy',
                 23: 'Squash : Powdery Mildew',
                 24: 'Strawberry : Leaf Scorch',
                 25: 'Strawberry : Healthy',
                 26: 'Tea : Anthracnose',
                 27: 'Tea : Bird Eye Spot',
                 28: 'Tea : Brown Blight',
                 29: 'Tea : Red Leaf Spot',
                 30: 'Tomato : Bacterial Spot',
                 31: 'Tomato : Early Blight',
                 32: 'Tomato : Late Blight',
                 33: 'Tomato : Leaf Mold',
                 34: 'Tomato : Septoria Leaf Spot',
                 35: 'Tomato : Spider Mites | Two-Spotted Spider Mite',
                 36: 'Tomato : Target Spot',
                 37: 'Tomato : Yellow Leaf Curl Virus',
                 38: 'Tomato : Mosaic Virus',
                 39: 'Tomato : Healthy'}



@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Load your trained model (replace 'load_model' with your actual model loading code)
        model = tf.keras.models.load_model("D:\Learnings\LeafLife\Final_Model.h5")
        
        # Preprocess the uploaded image
        img = tf.keras.preprocessing.image.load_img(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            target_size=(256, 256)  # Adjust based on your model's input size
        )
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        img_array = img_array / 255.0  # Normalize pixel values

        # Make predictions using the model
        predictions = model.predict(img_array)
        predicted_classes = predictions.argmax(axis=1)
        predicted_class_index = int(predicted_classes[0])
        
        if predicted_class_index in class_mapping :
            class_name = class_mapping[predicted_class_index]
            cure = disease_info.loc[predicted_class_index, 'possible_steps']
            description = disease_info.loc[predicted_class_index, 'description']

            class_msg = f'<b> PREDICTED CLASS: </b> <br>\n {class_name}'
            desc_msg = f'<b> DETAILS: </b> <br>\n {description}' 
            cure_msg = f'<b> POSSIBLE STEPS: </b> <br>\n {cure}'

            flash(class_msg, 'about_class')
            flash(desc_msg, 'about_disease')
            flash(cure_msg, 'about_cure')
            
            return render_template('action.html', filename=filename, predicted_class=class_name, details=description, actions=cure)
        else:
            flash('Class index not found in the mapping.')
            return redirect(request.url)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == '__main__':
    app.run(debug=True)