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


def index():
    return render_template('index.html', placeCode="")

def publish_map():
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    placeCode = request.form.get('placeCode')
    link = request.form.get('link')
    print(latitude,longitude,placeCode,link)
    map = Map(latitude=latitude,longitude=longitude,placeCode=placeCode,link=link)
    db.session.add(map)
    db.session.commit()
    return render_template('success.html')


def handle_form():
    placeCode = request.form.get('placeCode')
    print(placeCode)
    # Save to localStorage or perform any other action
    current_location = get_current_location()
    zoom_location = get_coordinates(placeCode)
    if current_location:
        currlatitude = current_location[0]
        currlongitude = current_location[1]
        latitude = zoom_location.json['latitude']
        longitude = zoom_location.json['longitude']
        print("lat: ",latitude,"long: ",longitude)
        return render_template('map.html',placeCode=placeCode,latitude=latitude,longitude=longitude,currlatitude=13.708096,currlongitude=79.594008)
    else:
        print("Unable to determine current location.")


    return render_template('index.html', placeCode=placeCode)

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
def publish_map():
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    placeCode = request.form.get('placeCode')
    link = request.form.get('link')
    print(latitude,longitude,placeCode,link)
    map = Map(latitude=latitude,longitude=longitude,placeCode=placeCode,link=link)
    db.session.add(map)
    db.session.commit()
    return render_template('success.html')


def handle_form():
    placeCode = request.form.get('placeCode')
    print(placeCode)
    # Save to localStorage or perform any other action
    current_location = get_current_location()
    zoom_location = get_coordinates(placeCode)
    if current_location:
        currlatitude = current_location[0]
        currlongitude = current_location[1]
        latitude = zoom_location.json['latitude']
        longitude = zoom_location.json['longitude']
        print("lat: ",latitude,"long: ",longitude)
        return render_template('map.html',placeCode=placeCode,latitude=latitude,longitude=longitude,currlatitude=13.708096,currlongitude=79.594008)
    else:
        print("Unable to determine current location.")


