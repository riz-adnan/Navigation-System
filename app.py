from flask import Flask, render_template, request, jsonify
import geocoder
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(80),  nullable=False)
    longitude = db.Column(db.String(120),  nullable=False)
    placeCode = db.Column(db.String(120), unique=True, nullable=False)
    link = db.Column(db.String(200), unique=True, nullable=False)
    def __repr__(self):
        return f"Map('{self.latitude}', '{self.longitude}', '{self.placeCode}',"

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

@app.route('/publish')
def publish():
    return render_template('post.html')

@app.route('/publish_map',methods=['POST'])
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

@app.route('/handle_form', methods=['POST'])
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
