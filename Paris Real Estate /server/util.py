import json
import pickle
import numpy as np
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Global variables
__locations = None
__model = None
__data_columns = None


def load_saved_artifacts():
    global __locations, __data_columns, __model
    print("Loading saved artifacts...start")
    try:
        with open("./artifacts/columns.json", "r") as f:
            __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[0:2]  # Exclude the first column if it's not a location

        with open("./artifacts/paris_real_estate_analysis.pickle", "rb") as f:
            __model = pickle.load(f)

        if __model is None:
            print("Error: Model is None after loading")

        print("Loading saved artifacts...done")
    except Exception as e:
        print(f"Error loading artifacts: {e}")
        __locations, __data_columns, __model = None, None, None

def get_coordinates(address):
    geolocator = Nominatim(user_agent="property_price_estimator")
    try:
        print(f"Geocoding address: {address}")  # 🔍 Print the address being searched
        location = geolocator.geocode(address, timeout=10)
        if location:
            print(f"Coordinates found: {location.latitude}, {location.longitude}")  # ✅ Success case
            return location.latitude, location.longitude
        else:
            print("Address not found.")
            return None, None
    except GeocoderTimedOut:
        print("Geocoder service timed out.")
        return None, None


def get_estimated_price(adresse_numero, adresse_nom_voie, code_postal, surface_reelle_bati, nombre_pieces_principales,
                        type_local, floor_level, condition):
    global __locations, __data_columns, __model

    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']

    if __data_columns is None or __model is None:
        print("Error: Artifacts not loaded properly")
        return None

    # Construct full address
    full_address = f"{adresse_numero} {adresse_nom_voie}, {code_postal} Paris, France"
    latitude, longitude = get_coordinates(full_address)

    if latitude is None or longitude is None:
        print("Could not determine coordinates. Please check the address.")
        return None

    print(f"📊 Creating feature array...")
    x = np.zeros(len(__data_columns))

    try:
        x[__data_columns.index("adresse_numero")] = adresse_numero
        x[__data_columns.index("code_postal")] = code_postal
        x[__data_columns.index("surface_reelle_bati")] = surface_reelle_bati
        x[__data_columns.index("nombre_pieces_principales")] = nombre_pieces_principales
        x[__data_columns.index("longitude")] = longitude
        x[__data_columns.index("latitude")] = latitude

        if "appartement" in __data_columns:
            x[__data_columns.index("appartement")] = 1 if type_local.lower() == "appartement" else 0
        if "maison" in __data_columns:
            x[__data_columns.index("maison")] = 1 if type_local.lower() == "maison" else 0

        print(f"🛠 Final feature array: {x}")

    except ValueError as e:
        print(f"❌ Error: {e}")
        return None

    # Predict price
    base_price = __model.predict([x])[0]
    print(f"📈 Base predicted price: {base_price}")

    # Apply adjustments for floor and condition
    floor_coefficients = {
        "Ground floor": 0.9,
        "1st to 3rd": 1.0,
        "4th to 5th": 1.1,
        "6th+": 1.15,
    }
    condition_coefficients = {
        "Need renovation": 0.9,
        "Good condition": 1.00,
        "Renovated": 1.15,
        "Luxury renovation": 1.25,
    }

    floor_factor = floor_coefficients.get(floor_level, 1.00)
    condition_factor = condition_coefficients.get(condition, 1.00)

    print(f"📏 Floor factor: {floor_factor}, Condition factor: {condition_factor}")

    final_price = base_price * floor_factor * condition_factor
    print(f"💰 Final estimated price: {final_price}")

    return round(final_price, 2)

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_estimated_price(148, "Avenue de Wagram", "75017", 88, 4, "Appartement", "1st to 3rd", "Renovated"))
