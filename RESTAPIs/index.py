from flask import Flask, request, jsonify

app = Flask(__name__)

countries = [
    {"id": '1', "name": "Thailand", "capital": "Bangkok"},
    {"id": '2', "name": "Australia", "capital": "Canberra"},
    {"id": '3', "name": "USA", "capital": "LA"},
]

def _find_next_id(id):
    data = [x for x in countries if x['id'] == id]
    return data

@app.route('/country/<id>', methods=["DELETE"])
def delete_country(id):
    data = _find_next_id(id)
    if not data:
        return {"error": "Country not found"}, 404
    countries.remove(data[0])
    return {"message": "Country deleted successfully"}, 200

@app.route('/country/<id>', methods=["PUT"])
def update_country(id):
    data = _find_next_id(id)
    if not data:
        return {"error": "Country not found"}, 404

    payload = request.get_json()
    name = payload.get('name')
    capital = payload.get('capital')

    data[0]['name'] = name
    data[0]['capital'] = capital
    return {"message": "Country updated successfully"}, 200

@app.route('/country/<id>', methods=["PATCH"])
def patch_country(id):
    data = _find_next_id(id)
    if not data:
        return {"error": "Country not found"}, 404

    payload = request.get_json()
    name = payload.get('name')
    capital = payload.get('capital')

    if name:
        data[0]['name'] = name
    if capital:
        data[0]['capital'] = capital
    return {"message": "Country updated successfully"}, 200

# REST API
@app.route('/country', methods=["GET"])
def get_country():
    return jsonify(countries)

# GET -by ID
@app.route('/country<id>', methods=["GET"])
def get_country_id(id):
    data = _find_next_id(id)
    return jsonify(data)

@app.route('/country', methods=["POST"])
def post_country():
    id = request.form.get('id')
    name = request.form.get('name')
    capital = request.form.get('capital')

    new_data = {
        "id": id,
        "name": name,
        "capital": capital,
        "complete": True
    }

    if (_find_next_id(id)):
        return {"error": "Bad Request"}, id
    else:
        countries.append(new_data)
        return jsonify(countries)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)