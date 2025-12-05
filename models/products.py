import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from db import db

class Products(db.Model):
    __tablename__ = "Products"

    product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    price = db.Column(db.Float())
    active = db.Column(db.Boolean(), default=True)

    company_id = db.Column(UUID(as_uuid=True),db.ForeignKey("Companies.company_id"),nullable=False)

    categories = db.relationship("Categories", secondary="ProductCategoryXref", backref="products")

    company = db.relationship("Companies", foreign_keys='[Products.company_id]', back_populates='products')

    warranty = db.relationship("Warranties", uselist=False, back_populates="product", cascade="all, delete")

    def __init__(self, product_name, description, price, company_id, active=True):
        self.product_name = product_name
        self.description = description
        self.price = price
        self.company_id = company_id
        self.active = active

    @staticmethod
    def new_product_obj():
        return Products('', '', 0, '', True)


class ProductsSchema(ma.Schema):
    product_id = ma.fields.UUID(dump_only=True)
    product_name = ma.fields.String(required=True)
    description = ma.fields.String()
    price = ma.fields.Float()
    active = ma.fields.Boolean()

    company = ma.fields.Nested("CompaniesSchema", exclude=['products'], dump_only=True)
    categories = ma.fields.Nested("CategoriesSchema", many=True, exclude=['products'], dump_only=True)
    warranty = ma.fields.Nested("WarrantiesSchema", allow_none=True, dump_only=True)

    class Meta:
        fields = ['product_id', 'product_name', 'description', 'price', 'active', 'company', 'categories', 'warranty']


product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)
