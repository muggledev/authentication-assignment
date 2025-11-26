from functools import wraps
from flask import request, jsonify
from models.users import Users
from models.auth_tokens import AuthTokens
from datetime import datetime, timezone
import uuid

def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization")
        if not header:
            return jsonify({"message": "missing token"}), 401

        token_str = header.replace("Bearer ", "").strip()

        try:
            token_uuid = uuid.UUID(token_str)
        except ValueError:
            return jsonify({"message": "invalid token format"}), 401

        auth = AuthTokens.query.filter_by(auth_token=token_uuid).first()
        if not auth:
            return jsonify({"message": "invalid token"}), 401

        if auth.expiration < datetime.now(timezone.utc):
            return jsonify({"message": "expired token"}), 401

        user = Users.query.get(auth.user_id)
        if not user:
            return jsonify({"message": "user not found"}), 401

        request.user = user
        return f(*args, auth_info=auth, **kwargs)
    return wrapper

def require_role(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not hasattr(request, "user") or request.user.role != role:
                return jsonify({"message": "not authorized"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
