import psycopg2
from yolomain import select_image
import base64


DATABASE_URL = "postgresql://postgres:admin1@localhost:5433/petfinder"


def process_images(animal_image):
    returned_json = {}
    animal_image = base64.b64decode(animal_image)

    returned_json["image"] = select_image(animal_image)
    return returned_json