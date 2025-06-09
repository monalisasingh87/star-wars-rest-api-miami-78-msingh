"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Person, Planet
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/users', methods=['GET'])
def get_users():

    all_users = User.query.all()

    if all_users is None:
        return jsonify('Sorry! No users found!'), 404
    else:
        all_users = list(map(lambda x: x.serialize(), all_users))
        return jsonify(all_users), 200
    

@api.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):

    current_user = db.session.get(User, user_id)

    if current_user is None:
        raise APIException('Sorry. User not found', status_code=404)
    
    all_people = [each_person.serialize() for each_person in current_user.favorite_people]
    
    response = {
        "message": f'User{current_user.username}\'s list of favorites people ',
        "data": {
            "favorite_people": all_people,
            "favorite_planets": all_planets, 
            }
         }
    
    return jsonify(response), 200


@api.route('/people', methods=['GET'])
def get_people():

    # query the database to get all the starwars characters
    all_people = Person.query.all()

    if all_people is None:
        return jsonify('Sorry! No Star Wars characters found!'), 404
    else:
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200


@api.route('/people/<int:person_id>', methods=['GET'])
def get_single_person(person_id):

    # query the database to get a SPECIFIC starwars character by id
    single_person = db.session.get(Person, person_id)

    if single_person is None:
        raise APIException(f'Person ID {person_id} was not found!', status_code=404)

    single_person = single_person.serialize()
    return jsonify(single_person), 200

@api.route('/favorite/people/<int:person_id>', methods=['POST'])
def add_favorite_person(person_id):

    user = request.get_json()
    user = db.session.get(User, user["user_id"])
    person = db.session.get(Person, person_id)

    user.favorite_people.append(person)
    db.session.commit()

    return jsonify(f'User {user.username}has added {person.name} to their favorites.'), 200


@api.route('/favorite/people/<int:person_id>', methods=['DELETE'])
def remove_favorite_person(person_id):

    user = request.get_json()
    user = db.session.get(User, user["user_id"])
   
    favorite = User.favorite_people.query.filter_by(person_id =person_id).first()
    db.session.delete(favorite)
    db.session.commit(), 

    return jsonify(f'User {user.username}has removed {favorite.name} from their favorites.'), 200


    



@api.route('/planet', methods=['GET'])
def get_planets():
    
    # query the database to get all the starwars planets
    all_planet = Planet.query.all()

    if all_planet is None:
        return jsonify('Sorry! No Star Wars planets found!'), 404
    else:
        all_planet = list(map(lambda x: x.serialize(), all_planet))
        return jsonify(all_planet), 200


@api.route('/planet/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    
     # query the database to get a SPECIFIC starwars planet by id
    single_planet = db.session.get(Planet, planet_id)

    if single_planet is None:
        raise APIException(f'Planet ID {planet_id} was not found!', status_code=404)

    single_planet = single_planet.serialize()
    return jsonify(single_planet), 200



@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    
    user = request.get_json()
    user = db.session.get(User, user["user_id"])
    Planet = db.session.get(Planet, planet_id)

    user.favorite_people.append(person)
    db.session.commit()

    return jsonify(f'User {user.username}has added {person.name} to their favorites.'), 200


@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    pass






