import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from db import db

class Warranties(db.Model):
    __tablename__ = "Warranties"

    warranty_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    warranty_name = db.Column(db.String(), nullable=False, unique=True)
    duration_months = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String())
    
    product_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("Products.product_id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    product = db.relationship("Products", back_populates="warranty")

    def __init__(self, warranty_name, duration_months, product_id, description=None):
        self.warranty_name = warranty_name
        self.duration_months = duration_months
        self.product_id = product_id
        self.description = description


class WarrantiesSchema(ma.Schema):
    warranty_id = ma.fields.UUID(dump_only=True)
    warranty_name = ma.fields.Str(required=True)
    duration_months = ma.fields.Int(required=True)
    description = ma.fields.Str()
    product_id = ma.fields.UUID(required=True)


warranty_schema = WarrantiesSchema()
warranties_schema = WarrantiesSchema(many=True)
