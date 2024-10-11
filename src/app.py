"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Initialize the family with the given members
initial_members = [
    {
        "id": jackson_family._generateId(),
        "first_name": "John",
        "age": 33,
        "lucky_numbers": [7, 13, 22]
    },
    {
        "id": jackson_family._generateId(),
        "first_name": "Jane",
        "age": 35,
        "lucky_numbers": [10, 14, 3]
    },
    {
        "id": jackson_family._generateId(),
        "first_name": "Jimmy",
        "age": 5,
        "lucky_numbers": [1]
    }
]

for member in initial_members:
    jackson_family.add_member(member)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"message": "Member not found"}), 404

@app.route('/member', methods=['POST'])
def add_member():
    member = request.json
    if not member:
        return jsonify({"message": "Invalid member data"}), 400
    new_member = jackson_family.add_member(member)
    return jsonify(new_member), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if jackson_family.delete_member(member_id):
        return jsonify({"done": True}), 200
    return jsonify({"message": "Member not found"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
