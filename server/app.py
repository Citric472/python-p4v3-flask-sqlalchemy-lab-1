from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_decoder = None  # This line is deprecated, consider customizing app.json_provider_class or app.json instead

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    # Query the database to get the earthquake by ID
    earthquake = Earthquake.query.get(id)

    if earthquake:
        # Return JSON response with earthquake data
        return jsonify({
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }), 200
    else:
        # Return JSON response indicating earthquake not found
        return jsonify({"message": f"Earthquake {id} not found."}), 404


@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    # Query the database to get all earthquakes with magnitude greater than or equal to the provided value
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    # Count the number of earthquakes
    count = len(earthquakes)

    # Prepare response data
    response_data = {
        "count": count,
        "quakes": []
    }

    # Append earthquake data to response
    for earthquake in earthquakes:
        response_data["quakes"].append({
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        })

    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)


