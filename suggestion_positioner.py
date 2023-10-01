import math

import psycopg2

from disappeared_animal import DisappearedAnimal
from founded_animal import FoundedAnimal
from new_similarity_check import calculate_location_points, get_similarity_score, get_images_by_animal_id

DATABASE_URL = 'postgresql://postgres:admin1@localhost:5433/petfinder'


class SuggestionPositioner:

    @classmethod
    def sort_suggested_animals(cls, disappeared_animal_id):
        disappeared_animal = cls.get_disappeared_animal(disappeared_animal_id)
        same_species_founded_animals = cls.get_same_species_founded_animals(disappeared_animal)
        filtered_animals = cls.filter_animal_by_location_score(disappeared_animal, same_species_founded_animals)
        return cls.sort_animal_by_similarity(disappeared_animal, filtered_animals)

    @classmethod
    def get_disappeared_animal(cls, disappeared_animal_id):
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()

            query = f"SELECT * FROM public."DisappearedAnimals" WHERE "DisappearedAnimalsId" = {disappeared_animal_id}"
            cursor.execute(query)

            animal = [
                DisappearedAnimal(
                    id=row[0],
                    latitude=row[1],
                    longitude=row[2],
                    date=row[3],
                    species_name=row[4],
                    owner_id=row[5],
                ) for row in cursor.fetchall()
            ][0]

            cursor.close()

            return animal

        except Exception as e:
            raise e

    @classmethod
    def get_same_species_founded_animals(cls, animal):
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()

            query = f"SELECT * FROM public."FoundedAnimals" WHERE "SpeciesName" = {animal.species_name}"
            cursor.execute(query)

            same_species_founded_animals = [
                FoundedAnimal(
                    id=row[0],
                    latitude=row[1],
                    longitude=row[2],
                    date=row[3],
                    species_name=row[4],
                    reporter_id=row[5],
                ) for row in cursor.fetchall()
            ]

            cursor.close()

            return same_species_founded_animals

        except Exception as e:
            raise e

    @classmethod
    def filter_animal_by_location_score(cls, disappeared_animal, founded_animals):
        filtered_founded_animals_dict = {}

        for animal in founded_animals:
            distance = cls.haversine_distance(disappeared_animal, animal)
            location_points = calculate_location_points(disappeared_animal.species_name, distance, time=None)
            if location_points > 0.02:
                filtered_founded_animals_dict[animal.id] = distance

        sorted_dict_by_value = {
            k: v for k, v in sorted(filtered_founded_animals_dict.items(), key=lambda item: item[1])
        }

        sorted_founded_animals_ids = list(sorted_dict_by_value.keys())
        animal_dict = {animal.animal_id: animal for animal in founded_animals if animal.id in sorted_founded_animals_ids}
        sorted_animals = [animal_dict[id_] for id_ in sorted_founded_animals_ids if id_ in animal_dict]

        return sorted_animals

    @classmethod
    def sort_animal_by_similarity(cls, disappeared_animal, founded_animals):
        similarity_dict = {}

        for founded_animal in founded_animals:
            disappeared_animal_image = get_images_by_animal_id(disappeared_animal.id, disappeared=True)
            founded_animal_image = get_images_by_animal_id(founded_animal.id, disappeared=False)
            similarity_score = get_similarity_score(disappeared_animal_image, founded_animal_image)

            similarity_dict[similarity_score] = founded_animal

        sorted_data = sorted(similarity_dict.items(), key=lambda x: x[0])

        return [item[1] for item in sorted_data]

    @classmethod
    def haversine_distance(cls, disappeared_animal, founded_animal):
        lat1 = disappeared_animal.latitude
        lon1 = disappeared_animal.longitude
        lat2 = founded_animal.latitude
        lon2 = founded_animal.longitude

        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        radius = 6371.0

        distance = radius * c

        return distance
