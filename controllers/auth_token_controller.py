from flask import jsonify
from db import db
from models.users import Users
from models.auth_tokens import AuthTokens
from datetime import datetime, timedelta, timezone
import uuid

def create_auth_token(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"message": "user not found"}), 404

    new_token = AuthTokens(
        auth_token=uuid.uuid4(),
        user_id=user.user_id,
        expiration=datetime.now(timezone.utc) + timedelta(hours=1)
    )

    db.session.add(new_token)
    db.session.commit()

    return jsonify({"message": "auth token created", "token": str(new_token.auth_token)}), 201
