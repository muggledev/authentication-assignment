from flask import Blueprint
import controllers.company_controller as controllers

companies = Blueprint("companies", __name__)

# CREATE COMPANY
@companies.route("/company", methods=["POST"])
def create_company_route():
    return controllers.create_company()

# GET ALL COMPANIES
@companies.route("/companies", methods=["GET"])
def get_companies_route():
    return controllers.get_companies()

# GET COMPANY BY ID
@companies.route("/company/<company_id>", methods=["GET"])
def get_company_by_id_route(company_id):
    return controllers.get_company_by_id(company_id)

# UPDATE COMPANY
@companies.route("/company/<company_id>", methods=["PUT"])
def update_company_route(company_id):
    return controllers.update_company(company_id)

# DELETE COMPANY
@companies.route("/company/<company_id>/delete", methods=["DELETE"])
def delete_company_route(company_id):
    return controllers.delete_company(company_id)
