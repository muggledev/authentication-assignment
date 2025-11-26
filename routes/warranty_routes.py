from flask import Blueprint
import controllers.warranty_controller as controllers

warranties = Blueprint("warranties", __name__)

# CREATE WARRANTY
@warranties.route("/warranty", methods=["POST"])
def create_warranty_route():
    return controllers.create_warranty()

# GET ALL WARRANTIES
@warranties.route("/warranties", methods=["GET"])
def get_warranties_route():
    return controllers.get_warranties()

# GET WARRANTY BY ID
@warranties.route("/warranty/<warranty_id>", methods=["GET"])
def get_warranty_by_id_route(warranty_id):
    return controllers.get_warranty_by_id(warranty_id)

# UPDATE WARRANTY
@warranties.route("/warranty/<warranty_id>", methods=["PUT"])
def update_warranty_route(warranty_id):
    return controllers.update_warranty(warranty_id)

# DELETE WARRANTY
@warranties.route("/warranty/<warranty_id>/delete", methods=["DELETE"])
def delete_warranty_route(warranty_id):
    return controllers.delete_warranty(warranty_id)
