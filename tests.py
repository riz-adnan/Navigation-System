def get_coordinates(placeCode):
    map_entry = Map.query.filter_by(placeCode=placeCode).first()

    if map_entry:
        return jsonify({
            'latitude': map_entry.latitude,
            'longitude': map_entry.longitude
        })
    else:
        return jsonify({'error': 'PlaceCode not found'}), 404

def get_current_location():
    # Using the built-in 'ipinfo' provider for IP-based location lookup
    location = geocoder.ip('me')

    if location.latlng:
        return location.latlng
    else:
        return None

# Example usage
current_location = get_current_location()

if current_location:
    print(f"Current Latitude: {current_location[0]}, Longitude: {current_location[1]}")
else:
    print("Unable to determine current location.")

@app.route('/')
def index():
    return render_template('index.html', placeCode="")
