import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from db import db

class Categories(db.Model):
    __tablename__ = "Categories"

    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.String())

    # products = db.relationship(
    #     "Products",
    #     secondary="ProductCategoryXref",
    #     back_populates="categories"
    # )

    def __init__(self, category_name, description=None):
        self.category_name = category_name
        self.description = description


class CategoriesSchema(ma.Schema):
    category_id = ma.fields.UUID(dump_only=True)
    category_name = ma.fields.Str(required=True)
    description = ma.fields.Str()
    products = ma.fields.Nested("ProductsSchema", many=True, exclude=["categories", "company", "warranty"])

category_schema = CategoriesSchema()
categories_schema = CategoriesSchema(many=True)
