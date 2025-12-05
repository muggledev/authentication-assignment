from flask import Blueprint
import controllers.auth_token_controller

auth_tokens = Blueprint("auth", __name__)

@auth_tokens.route("/auth", methods=["POST"])
def create_auth_token():
    return controllers.auth_token_controller.create_auth_token()
