from flask import Flask, request, jsonify
from similarity_check import process_images, process_location
import utils
from suggestion_positioner import SuggestionPositioner

app = Flask(__name__)


# Endpoint do przetwarzania danych z żądania GET
@app.route('/similarity_points', methods=['POST'])
def process_data():
    try:
        data = request.get_json()
        disappeared_animal_id = data.get("DisappearedAnimalId")
        founded_animal_ids = data.get("FoundedAnimalIds")

        if disappeared_animal_id is None or not founded_animal_ids:
            return jsonify({"error": f"Invaild input data - {disappeared_animal_id}, {founded_animal_ids}"}), 400

        result = process_images(disappeared_animal_id, founded_animal_ids)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/location_possibility', methods=['POST'])
def process_location_endpoint():
    try:
        data = request.get_json()
        disappeared_animal_id = data.get("DisappearedAnimalId")
        founded_animal_ids = data.get("FoundedAnimalIds")

        if disappeared_animal_id is None or not founded_animal_ids:
            return jsonify({"error": f"Invaild input data - {disappeared_animal_id}, {founded_animal_ids}"}), 400

        result = process_location(disappeared_animal_id, founded_animal_ids)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/select_image", methods=["POST"])
def process_image_framing():
    try:
        data = request.get_json()
        input_image = data.get("ImageBlob")

        if input_image is None:
            return (
                jsonify({"error": f"Invaild input data - {input_image}"}),
                400,
            )

        result = utils.process_images(input_image)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/sort_suggested_animals", methods=["POST"])
def sort_suggested_animals():
    try:
        data = request.get_json()
        disappeared_animal_id = data.get("DisappearedAnimalId")

        if disappeared_animal_id is None:
            return jsonify({"error": f"Invaild input data - {disappeared_animal_id}, {founded_animal_ids}"}), 400

        result = SuggestionPositioner.sort_suggested_animals(
            disappeared_animal_id=disappeared_animal_id
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)