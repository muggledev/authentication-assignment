import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from db import db

class Warranties(db.Model):
    __tablename__ = "Warranties"

    warranty_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    duration_months = db.Column(db.Integer(), nullable=False)
    
    product_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("Products.product_id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    product = db.relationship("Products", back_populates="warranty")

    def __init__(self, duration_months, product_id):
        self.duration_months = duration_months
        self.product_id = product_id
    
    def new_warranty_obj():
        return Warranties(0, '')


class WarrantiesSchema(ma.Schema):
    class Meta:
        fields = ['warranty_id', 'duration_months', 'product_id']
    warranty_id = ma.fields.UUID()
    duration_months = ma.fields.Integer(required=True)
    product_id = ma.fields.UUID(required=True)


warranty_schema = WarrantiesSchema()
warranties_schema = WarrantiesSchema(many=True)
