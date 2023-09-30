import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers
from tensorflow.keras.models import Model
from keras.layers import Dropout, Dense, GlobalAveragePooling2D
from keras.applications.inception_v3 import InceptionV3
import json

batch_size=64
data_dir = "animals"

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   validation_split=0.2,
                                   rotation_range=35,
                                   width_shift_range=0.25,
                                   preprocessing_function=tf.keras.applications.resnet.preprocess_input,
                                   height_shift_range=0.25,
                                   shear_range=0.25,
                                   zoom_range=0.25,
                                   horizontal_flip=True,
                                   fill_mode='nearest')
validation_datagen = ImageDataGenerator(rescale=1./255,validation_split=0.2)


train_generator = train_datagen.flow_from_directory(data_dir,
                                                    target_size=(299,299),
                                                    class_mode='categorical',
                                                    batch_size=batch_size,
                                                    subset="training")
validation_generator = validation_datagen.flow_from_directory(data_dir,
                                                              target_size=(299,299),
                                                              class_mode='categorical',
                                                              batch_size=batch_size,
                                                              subset="validation")

labels = {v: k for k, v in train_generator.class_indices.items()}

file_path = "labels.json"

# Zapisywanie słownika do pliku JSON
with open(file_path, 'w') as json_file:
    json.dump(labels, json_file)


testing_datagen = ImageDataGenerator(rescale = 1./255, validation_split=0)
testing_data = testing_datagen.flow_from_directory('dupa',
    target_size=(299,299),
    class_mode=None,
    batch_size=1,
    subset="training")
model = keras.models.load_model('FinalModel.h5')
for elem in testing_data:
    print(np.argmax(model.predict(elem)))