from flask import Flask, request, jsonify
from similarity_check import process_images


app = Flask(__name__)


# Endpoint do przetwarzania danych z żądania GET
@app.route('/similarity_points', methods=['GET'])
def process_data():
    try:
        data = request.get_json()
        searched_animal_id = data.get("searched_animal_id")
        found_animal_ids = data.get("found_animal_ids")

        if searched_animal_id is None or not found_animal_ids:
            return jsonify({"error": f"Invaild input data - {searched_animal_id}, {found_animal_ids}"}), 400

        result = process_images(searched_animal_id, found_animal_ids)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)