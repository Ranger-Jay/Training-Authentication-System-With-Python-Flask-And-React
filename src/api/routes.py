"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Planets, Vehicles, Characters
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS, cross_origin

api = Blueprint('api', __name__)
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = jsonify(message="Simple server is running")
    response_body.headers.add("Access-Control-Allow-Origin", "*")
    return response_body, 200


@api.route("/signup", methods=["POST"])
@cross_origin()
def signup():
    if request.method == 'POST':
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        #access_token = create_access_token(identity = email) 
        #access_token only needed after new user signs up

        if not email:
            return 'Email is required', 401
        if not password:
            return 'Password is required', 401
        
        email_query = User.query.filter_by(email=email).first()
        if email_query:
            return 'This email already exists' , 402

        user = User()
        user.email = email
        user.password = password
        user.is_active = True
        print(user)
        db.session.add(user)
        db.session.commit()

        response = {
            'message': 'User added successfully',
            'email': email
        }
        return jsonify(response), 200

@api.route('/login', methods=['POST'])
@cross_origin()

def sign_in():
    #this is the code we worked on in December 2022...but the new code allows us to see specifically which is the issue, either no email or no password 
    #Will update code after watching recording 1/06/22
    #body = request.get_json()
    #if body is None:
        #return jsonify({'Error: Body is empty'})

    #email = body['email']
    #password = body['password']

    ##alternate way 
    #user = User.query.filter_by(email = email, password = password).first()
    #if user is None:
        #return jsonify({'msg: Email or password are wrong'})


    if request.method == 'POST':
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        if not email:
            return 'Email is required', 401
        if not password:
            return 'Password is required', 401

    user = User.query.filter_by(email = email, password = password).first()
    if user is None:
        return 'error: This user was not found' , 401
    token = create_access_token(identity = user.id)
    print(token)
    return jsonify({
        "message" : "Successfully logged in." ,
        "token: " : token}), 200



@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    users = list(map(lambda index: index.serialize(), users))
    response_body = jsonify(users)
    response_body.headers.add("Access-Control-Allow-Origin", "*")
    return response_body, 200
    

# DELETE USER 
@api.route("/users/<int:user>/", methods=["DELETE"])
def delete_user(user):
    users = User.query.filter(User.id == user).first()
    if users is None:
        return jsonify({
            "message": "User does not exist"
        }), 404
    db.session.delete(users)
    db.session.commit()

    return jsonify({
        "message": "User was deleted successfully"
    }), 201
    
# GET 1 SPECIFIC USER
@api.route("/users/<int:user>/", methods=["GET"])
def get_specific_user(user):
    user = User.query.filter(User.id == user).first()

    if user is None:
        return jsonify({
            "message": "No user found"
        }), 404

    return jsonify({
        "user": user.serialize()
    }), 200
    
#GET route for Planets
@api.route("/planets", methods=["GET"])
@jwt_required()
def get_planets():
    planets = Planets.query.all()
    planets = list(map(lambda index: index.serialize(), planets))
    response_body = jsonify(planets)
    response_body.headers.add("Access-Control-Allow-Origin", "*")
    return response_body, 200
       

#POST for planets
@api.route("/planets", methods=["POST"])
@cross_origin()

def post_planets():
    if request.method == 'POST':
        planets_name = request.json.get('name', None)
        planets_diameter = request.json.get('diameter', None)
        planets_population = request.json.get('population', None)
        planets_climate = request.json.get('climate', None)
        planets_terrain = request.json.get('terrain', None)

        if not planets_name:
            return 'Planet name is required', 401
        if not planets_diameter:
            return 'Planet diameter is required', 401
        if not planets_population:
            return 'Planet population is required', 401
        if not planets_climate:
            return 'Planet climate is required', 401
        if not planets_terrain:
            return 'Planet terrain is required', 401

        
        planets_query = Planets.query.filter_by(name=planets_name).first()
        if planets_query:
            return 'This planet already exists' , 401

        planets = Planets()
        planets.name = planets_name
        planets.diameter = planets_diameter
        planets.population = planets_population
        planets.climate = planets_climate
        planets.terrain = planets_terrain
        print(planets)
        db.session.add(planets)
        db.session.commit()

        response = {
            'message': 'Planet added successfully',
            #'token': access_token,
            'planets_name': planets_name
        }
        return jsonify(response), 200

# DELETE Planets
@api.route("/planets/<int:planets>/", methods=["DELETE"])
def delete_planets(planets):
    planets = Planets.query.filter(Planets.id == planets).first()
    if planets is None:
        return jsonify({
            "message": "Planet does not exist"
        }), 404
    db.session.delete(planets)
    db.session.commit()

    return jsonify({
        "message": "Planet was deleted successfully"
    }), 201
            
# GET 1 SPECIFIC PLANET
@api.route("/planets/<int:planets>/", methods=["GET"])
@jwt_required()
def get_specific_planets(planets):
    planets = Planets.query.filter(Planets.id == planets).first()

    if planets is None:
        return jsonify({
            "message": "No planet found"
        }), 404

    return jsonify({
        "planet": planet.serialize()
    }), 200

#GET route for Vehicles
@api.route("/vehicles", methods=["GET"])
#LINE 213 how to limit what user sees, must have token in order to see Vehicles
@jwt_required()
def get_vehicles():
    vehicles = Vehicles.query.all()
    vehicles = list(map(lambda index: index.serialize(), vehicles))
    response_body = jsonify(vehicles)
    response_body.headers.add('Access-Control-Allow-Origin', '*')
    return response_body, 200


#POST route for Vehicles
@api.route("/vehicles", methods=["POST"])
@cross_origin()

def post_vehicles():
    if request.method == 'POST':
        vehicles_name = request.json.get('name', None)
        vehicles_length = request.json.get('length', None)
        vehicles_crew = request.json.get('crew', None)
        vehicles_passengers = request.json.get('passengers', None)
        vehicles_classification = request.json.get('classification', None)


        if not vehicles_name:
            return 'Vehicle name is required', 401
        if not vehicles_length:
            return 'Vehicle length is required', 401
        if not vehicles_crew:
            return 'Vehicle crew is required', 401
        if not vehicles_passengers:
            return 'Vehicle passengers is required', 401
        if not vehicles_classification:
            return 'Vehicle type is required', 401

        
        vehicles_query = Vehicles.query.filter_by(name=vehicles_name).first()
        if vehicles_query:
            return 'This vehicle already exists' , 401

        vehicles = Vehicles()
        vehicles.name = vehicles_name
        vehicles.length = vehicles_length
        vehicles.crew = vehicles_crew
        vehicles.passengers = vehicles_passengers
        vehicles.classification = vehicles_classification
        print(vehicles)
        db.session.add(vehicles)
        db.session.commit()

        response = {
            'message': 'Vehicle added successfully',
            #'token': access_token,
            'vehicles_name': vehicles_name
        }
        return jsonify(response), 200

#DELETE route for Vehicles
@api.route("/vehicles/<int:vehicles>/", methods=["DELETE"])
def delete_vehicles(vehicles):
    vehicles = Vehicles.query.filter(Vehicles.id == vehicles).first()
    if vehicles is None:
        return jsonify({
            "message": "Vehicle does not exist"
        }), 404
    db.session.delete(vehicles)
    db.session.commit()

    return jsonify({
        "message": "Vehicle was deleted successfully"
    }), 201

# GET 1 SPECIFIC VEHICLE
@api.route("/vehicles/<int:vehicles>/", methods=["GET"])
@jwt_required()
def get_specific_vehicles(vehicles):
    vehicles = Vehicles.query.filter(Vehicles.id == vehicles).first()

    if vehicles is None:
        return jsonify({
            "message": "No vehicle found"
        }), 404

    return jsonify({
        "vehicles": vehicles.serialize()
    }), 200

#GET route for Characters
@api.route("/characters", methods=["GET"])
@jwt_required()
def get_characters():
    characters = Characters.query.all()
    characters = list(map(lambda index: index.serialize(), characters))
    response_body = jsonify(characters)
    response_body.headers.add('Access-Control-Allow-Origin', '*')
    return response_body, 200
    

#POST route for Characters
@api.route("/characters", methods=["POST"])
def post_characters():
    if request.method == 'POST':
        characters_name = request.json.get('name', None)
        characters_gender = request.json.get('gender', None)
        characters_birth_year = request.json.get('birth year', None)
        characters_height = request.json.get('height', None)
        characters_homeworld = request.json.get('homeworld', None)


        if not characters_name:
            return 'Character name is required', 401
        if not characters_gender:
            return 'Character gender is required', 401
        if not characters_birth_year:
            return 'Character birth year is required', 401
        if not characters_height:
            return 'Character height is required', 401
        if not characters_homeworld:
            return 'Character homeworld is required', 401

        
        characters_query = Characters.query.filter_by(name=characters_name).first()
        if characters_query:
            return 'This character already exists' , 401

        characters = Characters()
        characters.name = characters_name
        characters.gender = characters_gender
        characters.birth.year = characters_birth_year
        characters.height = characters_height
        characters_homeworld = characters_homeworld
        print(characters)
        db.session.add(characters)
        db.session.commit()

        response = {
            'message': 'Character added successfully',
            #'token': access_token,
            'characters_name': characters_name
        }
        return jsonify(response), 200


#DELETE route for Characters
@api.route("/characters/<int:characters>/", methods=["DELETE"])
def delete_characters(characters):
    characters = Characters.query.filter(Characters.id == characters).first()
    if characters is None:
        return jsonify({
            "message": "Character does not exist"
        }), 404
    db.session.delete(characters)
    db.session.commit()

    return jsonify({
        "message": "Character was deleted successfully"
    }), 201


# GET 1 SPECIFIC Character
@api.route("/characters/<int:characters>/", methods=["GET"])
@jwt_required()
def get_specific_characters(characters):
    characters = Characters.query.filter(Characters.id == characters).first()

    if characters is None:
        return jsonify({
            "message": "No character found"
        }), 404

    return jsonify({
        "characters": characters.serialize()
    }), 200





#@api.route("/signup", methods=["POST"])
#def create_token():
    #email = request.json.get("email", None)
    #password = request.json.get("password", None)
    # Query your database for username and password. #We are expecting either GOOD or BAD email
    #email_check = User.query.filter_by(email=email, password=password).first() #1st email is name of column in table, #2 is email you are writing
    
    #if len(User.query.filter_by(email=email).all()) > 0: #if we find something > 0, will find what is below #User is the table                                              
    #if email is None:
        # the user was not found on the database
        #return jsonify({"msg": "Bad email or password"}), 401
    
    # create a new token with the user id inside #email is good/found
    #access_token = create_access_token(identity=email.id)
    #eturn jsonify({ "token": access_token, "email": email.id }), 200