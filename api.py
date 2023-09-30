from flask import Flask, request, jsonify
from similarity_check import process_images, process_location


app = Flask(__name__)


# Endpoint do przetwarzania danych z żądania GET
@app.route('/similarity_points', methods=['POST'])
def process_data():
    try:
        data = request.get_json()
        searched_animal_id = data.get("SearchedAnimalId")
        found_animal_ids = data.get("CurrentlyFoundAnimalIds")

        if searched_animal_id is None or not found_animal_ids:
            return jsonify({"error": f"Invaild input data - {searched_animal_id}, {found_animal_ids}"}), 400

        result = process_images(searched_animal_id, found_animal_ids)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/location_possibility', methods=['POST'])
def process_data():
    try:
        data = request.get_json()
        searched_animal_id = data.get("SearchedAnimalId")
        found_animal_ids = data.get("CurrentlyFoundAnimalIds")

        if searched_animal_id is None or not found_animal_ids:
            return jsonify({"error": f"Invaild input data - {searched_animal_id}, {found_animal_ids}"}), 400

        result = process_location(searched_animal_id, found_animal_ids)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)