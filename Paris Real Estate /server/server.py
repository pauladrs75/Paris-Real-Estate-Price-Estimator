from flask import Flask, request, jsonify
import util
from flask_cors import CORS
import sys
sys.stdout.flush()

app = Flask(__name__)
CORS(app)

util.load_saved_artifacts()

@app.route('/predict_home_price', methods=['OPTIONS'])
def handle_options():
    response = jsonify({})
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response
@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        print("✅ Received POST request")
        print("Form data received:", request.form)  # Debugging form data

        adresse_numero = int(request.form['adresse_numero'])
        adresse_nom_voie = request.form['adresse_nom_voie']
        code_postal = int(request.form['code_postal'])
        surface_reelle_bati = int(request.form['surface_reelle_bati'])
        nombre_pieces_principales = int(request.form['nombre_pieces_principales'])
        type_local = request.form['type_local']
        if type_local.lower() == "apartment":
            type_local = "Appartement"
        elif type_local.lower() == "house":
            type_local = "Maison"
        floor_level = request.form['floor_level']
        condition = request.form['condition'].capitalize()

        print(f"📍 Full address: {adresse_numero} {adresse_nom_voie}, {code_postal} Paris, France")

        estimated_price = util.get_estimated_price(
            adresse_numero, adresse_nom_voie, code_postal, surface_reelle_bati,
            nombre_pieces_principales, type_local, floor_level, condition
        )

        if estimated_price is None:
            print("❌ Price estimation failed")
            return jsonify({'error': 'Failed to estimate price'}), 400

        print(f"💰 Estimated price: {estimated_price} €")
        response = jsonify({'estimated_price': estimated_price})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except Exception as e:
        print(f"❌ Error: {str(e)}")  # Log the error
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("Starting Python Flask Server for Price Prediction...")
    app.run(debug=True)