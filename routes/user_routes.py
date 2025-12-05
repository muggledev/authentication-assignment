from flask import Blueprint
import controllers.user_controller as controllers

users = Blueprint("users", __name__)

# CREATE USER
@users.route("/user", methods=["POST"])
def create_user_route():
    return controllers.create_user()

# GET ALL USERS
@users.route("/users", methods=["GET"])
def get_users_route():
    return controllers.get_all_users()

# GET USER BY ID
@users.route("/user/<user_id>", methods=["GET"])
def get_user_by_id_route(user_id):
    return controllers.get_user_by_id(user_id)

# UPDATE USER
@users.route("/user/<user_id>", methods=["PUT"])
def update_user_route(user_id):
    return controllers.update_user(user_id=user_id)

# DELETE USER
@users.route("/user/<user_id>/delete", methods=["DELETE"])
def delete_user_route(user_id):
    return controllers.delete_user(user_id)
