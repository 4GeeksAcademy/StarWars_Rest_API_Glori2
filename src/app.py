"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

def get_post_users():
    if request.method == "GET":
        users_query = User.query.all()
        users = list(map(lambda user:user.serialize(),users_query))
        response_body = {
            "msg": "ok",
            "results": users
        }
        return jsonify(response_body), 200
    elif request.method == "POST":
        request_body = request.get_json(force=True)
        user = User(email=request_body["email"],password=request_body["password"],is_active=request_body["is_active"])
        if user is None:
            return jsonify({"msg":"El usuario no puede quedar vacío"}),400
        if "email" not in request_body:
            return jsonify({"msg":"El email no puede quedar vacío"}),400
        if "password" not in request_body:
            return jsonify({"msg":"La contraseña no puede quedar vacía"}),400
        db.session.add(user)
        db.session.commit()
        response_body = {
            "msg" : "ok - User created"
        }
        return jsonify(response_body), 200

@app.route("/planets", methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    planets_serialized = list(map(lambda x: x.serialize(), planets))
    return jsonify({"msg": 'Completed', "planets": planets_serialized})

@app.route("/planets", methods=['PUT'])
def modify_planet():
    body = request.get_json(silent=True)
    if body is None:
        raise APIException("El planeta no puede quedar vacío", status_code=400)
    if "id" not in body:
        raise APIException("Debes enviar el id del planeta", status_code=400)
    if "name" not in body:
        raise APIException("Debes enviar el nombre del planeta", status_code=400)
    one = Planet.query.get(body['id'])
    one.name = body['name']
    db.session.commit()
    return jsonify({"msg": "Completed"})

@app.route("/people", methods=["GET"])
def get_people():
    characters = People.query.all()
    characters_serialized = list(map(lambda x: x.serialize(), characters))
    return jsonify({"msg": 'Completed', "people": characters_serialized})

@app.route("/people", methods=['PUT'])
def modify_people():
    body = request.get_json(silent=True)
    if body is None:
        raise APIException("El personaje no puede quedar vacío", status_code=400)
    if "id" not in body:
        raise APIException("Debes enviar el id del personaje ", status_code=400)
    if "name" not in body:
        raise APIException("Debes enviar el nuevo nombre del personaje", status_code=400)
    one_character = Planet.query.get(body['id'])
    one_character.name = body['name']
    db.session.commit()
    return jsonify({"msg": "Completed"})

@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorites_query = Favorite.query.all()
    favorites_serialized = list(map(lambda favorite:favorite.serialize(),favorites_query))
    response_body = {
        "msg": "ok",
        "results": favorites_serialized
    }
    return jsonify(response_body), 200

@app.route('/favorites', methods=['PUT'])
def mod_favorites():
    request_body = request.get_json(force=True)
    exists = Favorite.query.filter_by(user_id=request_body["user_id"],people_id=request_body["people_id"],planet_id=request_body["planet_id"]).first()
    if exists != None:
        return jsonify({"msg":"El personaje ya existe"}),400
    favorite = Favorite(user_id=request_body["user_id"],people_id=request_body["people_id"],planet_id=request_body["planet_id"])
    if favorite.user_id is None:
        return jsonify({"msg":"Debe seleccionar un usuario"}),400
    if favorite.character_id is None and favorite.planet_id is None:
        return jsonify({"msg":"Debe seleccionar un personaje o planeta"}),400
    if favorite.character_id is not None and favorite.planet_id is not None:
        return jsonify({"msg":"Multiples opciones seleccionadas"}),400
    db.session.add(favorite)
    db.session.commit()
    response_body = {
        "msg" : "ok - Favorite created"
    }
    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
