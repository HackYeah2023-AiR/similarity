import psycopg2
from yolomain import select_image
import base64


DATABASE_URL = "postgresql://postgres:admin1@localhost:5433/petfinder"


def process_images(animal_image):
    returned_json = {}
    animal_image = base64.b64decode(animal_image)

    returned_json["image"] = select_image(animal_image)
    return returned_json


def get_images_by_animal_ids(animal_ids):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        query = "SELECT animal_img_id FROM WildAnimal WHERE animal_id = {animal_id}"

        cursor.execute(query)
        image_id = [row[0] for row in cursor.fetchall()]
        query = "SELECT image FROM AnimalImage WHERE animal_img_id = {image_id[0]}"
        cursor.execute(query)
        image = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()

        return image[0], image_id[0]
    except Exception as e:
        return []
