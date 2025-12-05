from flask import jsonify, request
from flask_bcrypt import generate_password_hash
from db import db
from models.users import Users, user_schema, users_schema
from models.auth_tokens import AuthTokens
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth
import datetime


def create_user():
    post_data = request.form if request.form else request.json

    new_user = Users.new_user_obj()
    populate_object(new_user, post_data)

    new_user.password = generate_password_hash(new_user.password).decode('utf8')

    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to add user"}), 400

    return jsonify({"message": "user created", "user": user_schema.dump(new_user)}), 201


@authenticate
def get_all_users():
    users = db.session.query(Users).all()
    return jsonify({"users": users_schema.dump(users)}), 200


@authenticate_return_auth
def get_user_by_id(user_id, auth_info):
    user = db.session.query(Users).filter(Users.user_id == user_id).first()

    if not user:
        return jsonify({"message": "user not found"}), 404

    if auth_info.user.role == "admin" or str(auth_info.user.user_id) == user_id:
        return jsonify({"user": user_schema.dump(user)}), 200

    return jsonify({"message": "not authorized"}), 403


@authenticate_return_auth
def update_user(user_id, auth_info):
    post_data = request.form if request.form else request.json
    user = db.session.query(Users).filter(Users.user_id == user_id).first()

    if not user:
        return jsonify({"message": "user not found"}), 404

    if auth_info.user.role != "admin" and str(auth_info.user.user_id) != user_id:
        return jsonify({"message": "not authorized"}), 403


    if post_data.get('password'):
        user.password = generate_password_hash(post_data.get('password')).decode('utf8')

    populate_object(user, post_data)
    db.session.commit()

    return jsonify({"message": "user updated", "user": user_schema.dump(user)}), 200


@authenticate_return_auth
def delete_user(user_id, auth_info):
    user = db.session.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        return jsonify({"message": "user not found"}), 404

    if auth_info.user.role != "admin" and str(auth_info.user.user_id) != user_id:
        return jsonify({"message": "not authorized"}), 403

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "user deleted"}), 200
