from flask import Flask, request, jsonify, Blueprint
from api.models import db, User
from flask_cors import CORS
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

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

        new_user = User(email=email)
        new_user.set_password(password)
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

        access_token = create_access_token(identity=str(user.id))
        return jsonify({"token": access_token}), 200

    except Exception as e:
        return jsonify({"msg": "Error interno del servidor", "error": str(e)}), 500

@api.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    if not user:
        return jsonify({"msg", "usuario no encontrado"}), 404
    return jsonify({"msg": f"Bienvenido a la zona privada, usuario {current_user_id}"}), 200
