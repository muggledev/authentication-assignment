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

    def __init__(self, email, password, role='user'):
        self.email = email
        self.password = password
        self.role = role

    def new_user_obj():
        return Users('', '', 'user')

class UsersSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'email', 'role']
    user_id = ma.fields.UUID()
    email = ma.fields.String()
    role = ma.fields.String()

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
