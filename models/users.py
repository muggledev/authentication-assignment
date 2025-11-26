import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma

class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), default="user")

class UsersSchema(ma.Schema):
    user_id = ma.fields.UUID()
    email = ma.fields.Str()
    role = ma.fields.Str()

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
