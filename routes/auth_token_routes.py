from flask import Blueprint
import controllers.auth_token_controller as auth_token_controller

auth_tokens = Blueprint("auth_tokens", __name__)

@auth_tokens.route("/auth", methods=["POST"])
def create_auth_token_route():
    from flask import request
    data = request.get_json() or request.form
    user_id = data.get("user_id")
    return auth_token_controller.create_auth_token(user_id)
