from flask import Flask, render_template, request
import os
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import cv2

model = load_model("model.h5")

def predict(file_name):
    img = cv2.imread(file_name)
    img = cv2.resize(img,(150,150))
    img = img_to_array(img)/255
    img = np.expand_dims(img,axis=0)
    prediction = model.predict(img)
    
    prediction = prediction[0]
    
    return int(prediction >= 0.5)
    


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_img():
    img = request.files['image']
    img_name = img.filename
    
    path = os.path.join('static/images/',img_name)
    img.save(path)    
    
    prediction = predict(path)
    
    if prediction == 0:
        pred = "Prediction : Diseased Cotton Leaf"
    else :
        pred = "Prediction : Fresh Cotton Leaf"
    
    return render_template("index.html", img_src = path, result = pred)


if __name__ == "__main__":
    app.run()