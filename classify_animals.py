import numpy as np
import time
from keras.models import load_model
from PIL import Image
import json
import os
from io import BytesIO


SIZE = (299, 299)


def get_box(input_image_name):
    yolo = load_model("FinalModel.h5")
    image_src = Image.open(BytesIO(input_image_name))
    image_thumb = image_src.resize(SIZE, Image.BICUBIC)

    image = np.array(image_thumb, dtype="float32")
    image /= 255.0
    image = np.expand_dims(image, axis=0)
    with open("labels.json", 'r') as json_file:
        labels = json.load(json_file)

    output = labels[str(np.argmax(yolo.predict(image)))]
    return output


def select_image(input_image_name):
    prediction = get_box(input_image_name)
    return prediciton

