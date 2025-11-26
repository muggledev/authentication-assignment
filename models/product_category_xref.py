import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db

class ProductCategoryXref(db.Model):
    __tablename__ = "ProductCategoryXref"

    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Products.product_id", ondelete="CASCADE"), primary_key=True)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Categories.category_id", ondelete="CASCADE"), primary_key=True)
