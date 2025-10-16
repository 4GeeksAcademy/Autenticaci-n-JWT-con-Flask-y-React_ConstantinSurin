from flask import Flask, request, jsonify, Blueprint
from api.models import db, User
from api.utils import APIException
from flask_cors import CORS
from flask_bcrypt import generate_password_hash, check_password_hash

api = Blueprint('api', __name__)
CORS(api, resources={r"/api/*": {"origins": "*"}})

@api.route('/signup', methods=["POST"])
def signup():
    try:
        data = request.get_json(force=True)
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"msg": "Email y password son requeridos"}), 400

        existing_user = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar_one_or_none()

        if existing_user:
            return jsonify({"msg": "Usuario ya existe"}), 400

        new_user = User(email = data["email"], password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "Usuario creado correctamente"}), 201

    except Exception as e:
        return jsonify({"msg": "Error interno del servidor", "error": str(e)}), 500


@api.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"msg": "Email y password son requeridos"}), 400

        user = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar_one_or_none()

        if user is None:
            return jsonify({"msg": "Usuario no encontrado"}), 404

        if not check_password_hash(user.password_hash, password):
            return jsonify({"msg": "Contraseña incorrecta"}), 401

        return jsonify({"token": "abc123"}), 200

    except Exception as e:
        return jsonify({"msg": "Error interno del servidor", "error": str(e)}), 500
    

@api.route('/profile', methods=['GET'])
def private():
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"msg": "Token no proporcionado"}), 401

    token = auth_header.split(" ")[1]

    # En un caso real aquí validarías el JWT
    if token != "abc123":
        return jsonify({"msg": "Token inválido"}), 403

    return jsonify({"msg": "Bienvenido a la zona privada"}), 200
