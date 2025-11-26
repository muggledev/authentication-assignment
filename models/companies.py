import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from db import db

class Companies(db.Model):
    __tablename__ = "Companies"

    company_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = db.Column(db.String(), nullable=False, unique=True)
    address = db.Column(db.String())
    email = db.Column(db.String())

    products = db.relationship("Products", back_populates="company", cascade="all, delete-orphan")

    def __init__(self, company_name, address=None, email=None):
        self.company_name = company_name
        self.address = address
        self.email = email


class CompaniesSchema(ma.Schema):
    company_id = ma.fields.UUID(dump_only=True)
    company_name = ma.fields.Str(required=True)
    address = ma.fields.Str()
    email = ma.fields.Str()
    products = ma.fields.Nested("ProductsSchema", many=True, exclude=["company", "categories", "warranty"])

company_schema = CompaniesSchema()
companies_schema = CompaniesSchema(many=True)
