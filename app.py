from flask import Flask, render_template, request
import os
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np
import cv2
from keras.preprocessing.image import img_to_array
from keras.models import load_model

model = load_model("model.h5")

def predict(filepath):
  img = plt.imread(filepath)
  temp_img = img
  img = cv2.resize(img,(150,150))
  img = img_to_array(img)/255
  img = np.expand_dims(img,axis=0)
  prediction = model.predict(img) >= 0.5
  if prediction==1:
    prediction = "Fresh Cotton Leaf"
    print("Prediction: "+prediction)
    return 1
  else:
    prediction = "Diseased Cotton Leaf"
    print("Prediction: "+prediction)
    return 0
  

    


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
