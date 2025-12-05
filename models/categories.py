import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from db import db

class Categories(db.Model):
    __tablename__ = "Categories"

    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_name = db.Column(db.String(), nullable=False, unique=True)

    def __init__(self, category_name):
        self.category_name = category_name

    @staticmethod
    def new_category_obj():
        return Categories('')


class CategoriesSchema(ma.Schema):
    category_id = ma.fields.UUID(dump_only=True)
    category_name = ma.fields.String(required=True)
    products = ma.fields.Nested("ProductsSchema", many=True, exclude=['categories', 'company', 'warranty'], dump_only=True)

    class Meta:
        fields = ['category_id', 'category_name', 'products']


category_schema = CategoriesSchema()
categories_schema = CategoriesSchema(many=True)
