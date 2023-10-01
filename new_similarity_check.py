import numpy as np
import psycopg2

from io import BytesIO
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.preprocessing import image


DATABASE_URL = 'postgresql://postgres:admin1@localhost:5433/petfinder'


def get_images_by_animal_id(animal_id, disappeared=False):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        if disappeared:
            query = f'SELECT "ImageBlob" FROM pubilc."AnimalImages" WHERE "DisappearedAnimalEntityDisappearedAnimalId" = {animal_id}'
        else:
            query = f'SELECT "ImageBlob" FROM public."AnimalImages" WHERE "FoundedAnimalEntityFoundedAnimalId" = {animal_id}'
        cursor.execute(query)
        image = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()

        return image[0]
    except Exception as e:
        raise e


def calculate_location_points(species_name, distance, time=None):
    # include time
    if species_name == "cat":
        return 1/(distance + 0.01)*1.3
    elif species_name == "dog":
        return 1/(distance + 0.01)*1.1
    return 1


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


def get_image_embeddings(object_image: image, model):
    """
      -----------------------------------------------------
      convert image into 3d array and add additional dimension for model input
      -----------------------------------------------------
      return embeddings of the given image
    """

    image_array = np.expand_dims(image.img_to_array(object_image), axis=0)
    image_embedding = model.predict(image_array)

    return image_embedding


def get_similarity_score(first_image: str, second_image: str, model):
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

    similarity_score = cosine_similarity(first_image_vector, second_image_vector).reshape(1, )

    return similarity_score
