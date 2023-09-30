import numpy as np 
from PIL import Image
from tensorflow.keras.preprocessing import image
from io import BytesIO

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from keras.applications.vgg16 import VGG16
from sklearn.metrics.pairwise import cosine_similarity
import psycopg2


DATABASE_URL = 'postgresql://username:password@localhost:5432/yourdatabase'


def get_images_by_animal_ids(animal_ids):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        query = "SELECT image FROM animal_images WHERE animal_id == %s"
        cursor.execute(query, animal_ids)
        image = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()

        return image
    except Exception as e:
        return []


def process_images(searched_animal_id, found_animal_ids):
    vgg16 = VGG16(weights='imagenet', include_top=False, 
                  pooling='max', input_shape=(224, 224, 3))
    searched_image = get_images_by_animal_ids(searched_animal_id)
    
    for model_layer in vgg16.layers:
        model_layer.trainable = False
    returned_json = {"searched_id": searched_animal_id}
    for id in found_animal_ids:
        found_images = get_images_by_animal_ids(id)
        returned_json[id] = get_similarity_score(searched_image, found_images, vgg16)
    return returned_json


def load_image(image_path):
    """
        -----------------------------------------------------
        Process the image provided. 
        - Resize the image 
        -----------------------------------------------------
        return resized image
    """
    input_image = Image.open(BytesIO(image_path))
    resized_image = input_image.resize((224, 224))
    return resized_image


def get_image_embeddings(object_image : image, model):

    """
      -----------------------------------------------------
      convert image into 3d array and add additional dimension for model input
      -----------------------------------------------------
      return embeddings of the given image
    """

    image_array = np.expand_dims(image.img_to_array(object_image), axis = 0)
    image_embedding = model.predict(image_array)

    return image_embedding


def get_similarity_score(first_image : str, second_image : str, model):
    """
        -----------------------------------------------------
        Takes image array and computes its embedding using VGG16 model.
        -----------------------------------------------------
        return embedding of the image
 
    """

    first_image = load_image(first_image)
    second_image = load_image(second_image)

    first_image_vector = get_image_embeddings(first_image, model)
    second_image_vector = get_image_embeddings(second_image, model)

    similarity_score = cosine_similarity(first_image_vector, second_image_vector).reshape(1,)

    return similarity_score


# def show_image(image_path):
#     image = mpimg.imread(image_path, 0)
#     imgplot = plt.imshow(image)
#     plt.show()


# # define the path of the images
# sunflower = 'pies1.jpg'
# helianthus = 'drzewo1.jpg'

# # tulip = '/content/Tulip.jpeg'

# # use the show_image function to plot the images
# show_image(sunflower), show_image(helianthus)

# similarity_score = get_similarity_score(sunflower, helianthus)
# print(similarity_score)