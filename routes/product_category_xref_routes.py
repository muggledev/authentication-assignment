from flask import Blueprint
import controllers.product_category_xref_controller as controllers

product_category_xref = Blueprint("product_category_xref", __name__)

@product_category_xref.route("/product/category", methods=["POST"])
def add_product_category_route():
    return controllers.add_product_category()

@product_category_xref.route("/product/category/delete", methods=["DELETE"])
def remove_product_category_route():
    return controllers.remove_product_category()
