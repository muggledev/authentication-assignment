from flask import Blueprint
import controllers.category_controller as controllers

categories = Blueprint("categories", __name__)

# CREATE CATEGORY
@categories.route("/category", methods=["POST"])
def create_category_route():
    return controllers.create_category()

# GET ALL CATEGORIES
@categories.route("/categories", methods=["GET"])
def get_categories_route():
    return controllers.get_categories()

# GET CATEGORY BY ID
@categories.route("/category/<category_id>", methods=["GET"])
def get_category_by_id_route(category_id):
    return controllers.get_category_by_id(category_id)

# UPDATE CATEGORY
@categories.route("/category/<category_id>", methods=["PUT"])
def update_category_route(category_id):
    return controllers.update_category(category_id)

# DELETE CATEGORY
@categories.route("/category/<category_id>/delete", methods=["DELETE"])
def delete_category_route(category_id):
    return controllers.delete_category(category_id)
