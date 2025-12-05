import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma

class AuthTokens(db.Model):
    __tablename__ = "AuthTokens"

    auth_token = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"))
    expiration = db.Column(db.DateTime(), nullable=False)

    user = db.relationship("Users", backref="tokens")

    def __init__(self, user_id, expiration):
        self.user_id = user_id
        self.expiration = expiration

class AuthTokenSchema(ma.Schema):
    class Meta:
        fields = ['auth_token', 'expiration', 'user']
    auth_token = ma.fields.UUID()
    expiration = ma.fields.DateTime(required=True)
    user = ma.fields.Nested('UsersSchema')

auth_token_schema = AuthTokenSchema()