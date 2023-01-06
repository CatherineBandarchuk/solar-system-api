from app import db
from app.models.planet import Planet
from app.models.moon import Moon
from flask import Blueprint, jsonify, abort, make_response, request

planets_bp = Blueprint("planets_bp", __name__, url_prefix = "/planets")

# Helper functions
# Validating the id of the planet: id needs to be int and exists the planet with the id.
# Returning the valid Planet instance if valid id
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(jsonify(f"{cls.__name__} {model_id} invalid"), 400))
    class_obj = cls.query.get(model_id)
    if not class_obj:
        abort(make_response(jsonify(f"{cls.__name__} {model_id} not found"), 404))
    return class_obj

# Validating the user input to create or update the table planet
# Returning the valid JSON if valid input
def validate_input(planet_value):
    if "name" not in planet_value \
        or not isinstance(planet_value["name"], str) \
        or planet_value["name"] == "" \
        or "length_of_year" not in planet_value \
        or not isinstance(planet_value["length_of_year"], int) \
        or planet_value["length_of_year"] <=0 \
        or "description" not in planet_value \
        or not isinstance(planet_value["description"], str) \
        or planet_value["description"] == "":
        return abort(make_response(jsonify("Invalid request"), 400))  
    return planet_value

# Routes functions
# Creating new record in the database Planet
@planets_bp.route("", methods = ["POST"])
def create_planet():
    planet_value = validate_input(request.get_json())
    new_planet = Planet.from_dict(planet_value)

    db.session.add(new_planet)
    db.session.commit()
    return make_response(jsonify(f"Planet {new_planet.name} successfully created"), 201)    

# Get all planets info
# Return JSON list
@planets_bp.route("", methods = ["GET"])
def get_planets_query():
    planet_query = Planet.query
    # Filtering by name (return all records which name contains planet_name_query)
    planet_name_query = request.args.get("name")

    if planet_name_query:
        planet_query = planet_query.filter(Planet.name.ilike(f"%{planet_name_query}%"))
    
    sort_by_name_query = request.args.get("sort_by_name")
    if sort_by_name_query == "desc":
        planet_query = planet_query.order_by(Planet.name.desc()).all()
    elif sort_by_name_query == "asc":
        planet_query = planet_query.order_by(Planet.name).all()

    sort_by_length_of_year_query = request.args.get("sort_by_length_of_year")
    if sort_by_length_of_year_query == "desc":
        planet_query = planet_query.order_by(Planet.length_of_year.desc()).all()
    elif sort_by_length_of_year_query == "asc":
        planet_query = planet_query.order_by(Planet.length_of_year).all() 
    
    planet_response = []
    for planet in planet_query:
        planet_response.append(planet.to_dict())

    return jsonify(planet_response), 200

# Read one planet 
# Return one planet info in JSON format    
@planets_bp.route("/<planet_id>",methods=["GET"] )
def get_one_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    return planet.to_dict()

# Update one planet
@planets_bp.route("/<planet_id>",methods=["PUT"] )
def update_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = validate_input(request.get_json())

    planet.name = request_body["name"]
    planet.length_of_year = request_body["length_of_year"]
    planet.description = request_body["description"]
    
    db.session.commit()
    return make_response(jsonify(f"Planet {planet_id} successfully updated"), 200)   
    
# Delete one planet
@planets_bp.route("/<planet_id>",methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    db.session.delete(planet)
    db.session.commit()

    return make_response(jsonify(f"Planet {planet.id} successfully deleted"), 200)

@planets_bp.route("/<planet_id>/moons", methods=["POST"])
def add_new_cat_to_caretaker(planet_id):
    planet = validate_model(Planet, planet_id)

    request_body = request.get_json()
    moon = Moon.from_dict(request_body)
    moon.planet = planet

    db.session.add(moon)
    db.session.commit()

    message = f"Cat {moon.name} created with Caretaker {planet.name}"
    return make_response(jsonify(message), 201)

@planets_bp.route("/<planet_id>/moons", methods=["GET"])
def get_all_moons_for_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    moons_response = []
    for moon in planet.moons:
        moons_response.append(moon.to_dict())

    return jsonify(moons_response)