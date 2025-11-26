from flask import jsonify, request
from flask_bcrypt import generate_password_hash
from db import db
from models.users import Users, user_schema, users_schema
from models.auth_tokens import AuthTokens
from util.reflection import populate_object
from lib.authenticate import authenticate, require_role
import datetime


def create_user():
    data = request.get_json() or request.form

    new_user = Users()
    populate_object(new_user, data)

    if not new_user.password:
        return jsonify({"message": "password is required"}), 400

    new_user.password = generate_password_hash(new_user.password).decode('utf8')
    if not new_user.role:
        new_user.role = "user"

    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to add user"}), 400

    return jsonify({"message": "user created", "user": user_schema.dump(new_user)}), 201


@authenticate
@require_role("admin")
def get_all_users(auth_info):
    users = Users.query.all()
    return jsonify({"users": users_schema.dump(users)}), 200


@authenticate
def get_user_by_id(user_id, auth_info):
    user = Users.query.get(user_id)

    if not user:
        return jsonify({"message": "user not found"}), 404

    if request.user.role == "admin" or str(request.user.user_id) == user_id:
        return jsonify({"user": user_schema.dump(user)}), 200

    return jsonify({"message": "not authorized"}), 403


@authenticate
def update_user(user_id, auth_info):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"message": "user not found"}), 404

    if request.user.role != "admin" and str(request.user.user_id) != user_id:
        return jsonify({"message": "not authorized"}), 403

    data = request.get_json() or request.form

    if "password" in data:
        data["password"] = generate_password_hash(data["password"]).decode('utf8')

    populate_object(user, data)
    db.session.commit()

    return jsonify({"message": "user updated", "user": user_schema.dump(user)}), 200


@authenticate
def delete_user(user_id, auth_info):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"message": "user not found"}), 404

    if request.user.role != "admin" and str(request.user.user_id) != user_id:
        return jsonify({"message": "not authorized"}), 403

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "user deleted"}), 200
