"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/signup', methods=["POST"])
def signup():
    data = request.get_json()

    if not data.get("email") or not data.get("password"):
        return jsonify({"msg": "Email y password son requeridos"}), 400

    existing_user = db.session.execute(
        db.select(User).where(User.email == data["email"])
    ).scalar_one_or_none()

    if existing_user:
        return jsonify({"msg": "User with this email already exists"}), 400

    new_user = User(email=data["email"])
    new_user.set_password(data["password"])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201
