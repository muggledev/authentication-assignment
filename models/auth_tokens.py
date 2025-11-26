import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.dialects.postgresql import UUID
from db import db

class AuthTokens(db.Model):
    __tablename__ = "AuthTokens"

    auth_token = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"))
    expiration = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc) + timedelta(hours=2)
    )

    user = db.relationship("Users", backref="tokens")
