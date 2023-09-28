from flask import Flask, redirect, request, render_template
# from tensorflow.keras.models import load_model  # Import the function to load the model
# import numpy as np
# from PIL import Image
# import io

app = Flask(__name__)

# model = load_model("D:\Learnings\LeafLife\Final_Model.h5")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/portfolio-details')
def portfolio_details():
    return render_template('portfolio-details.html')

@app.route('/action')
def action():
    return render_template('action.html')

# # Function to preprocess the uploaded image
# def preprocess_image(image):
#     # Load the image and resize it to the required input size of your model
#     img = Image.open(image)
#     img = img.resize((224, 224))  # Adjust the size based on your model's input size
#     img = np.array(img) / 255.0  # Normalize pixel values (assuming model expects values between 0 and 1)
#     img = img.reshape(1, 224, 224, 3)  # Reshape for model input (adjust the shape if needed)
#     return img

# # Function to get predictions
# def predict_disease(image):
#     # Preprocess the image
#     processed_image = preprocess_image(image)
    
#     # Make predictions using the loaded model
#     predictions = model.predict(processed_image)
    
#     # You may need to post-process the predictions based on your model's output format

#     return predictions

# @app.route('/predict', methods=['POST'])
# def predict():
#     if 'image' not in request.files:
#         return redirect(request.url)
    
#     image = request.files['image']
    
#     if image.filename == '':
#         return redirect(request.url)
    
#     # Get predictions
#     predictions = predict_disease(image)

#     # Process predictions and get the predicted class
#     predicted_class = process_predictions(predictions)  # Implement this function as per your model's output

#     # Retrieve information based on the predicted class
#     disease_info = get_disease_info(predicted_class)  # Implement this function as described earlier

#     return render_template('action.html', image=image, predicted_class=predicted_class, disease_info=disease_info)

if __name__ == '__main__':
    app.run(debug=True)