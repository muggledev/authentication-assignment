from flask import Blueprint
import controllers.product_controller as controllers

products = Blueprint("products", __name__)

# CREATE PRODUCT
@products.route("/product", methods=["POST"])
def create_product_route():
    return controllers.create_product()

# GET ALL PRODUCTS
@products.route("/products", methods=["GET"])
def get_products_route():
    return controllers.get_products()

# GET ACTIVE PRODUCTS
@products.route("/products/active", methods=["GET"])
def get_active_products_route():
    return controllers.get_active_products()

# GET PRODUCT BY ID
@products.route("/product/<product_id>", methods=["GET"])
def get_product_by_id_route(product_id):
    return controllers.get_product_by_id(product_id)

# GET PRODUCTS BY COMPANY
@products.route("/product/company/<company_id>", methods=["GET"])
def get_products_by_company_route(company_id):
    return controllers.get_products_by_company(company_id)

# UPDATE PRODUCT
@products.route("/product/<product_id>", methods=["PUT"])
def update_product_route(product_id):
    return controllers.update_product(product_id)

# DELETE PRODUCT
@products.route("/product/<product_id>/delete", methods=["DELETE"])
def delete_product_route(product_id):
    return controllers.delete_product(product_id)
