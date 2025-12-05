from flask import request, jsonify
from db import db
from models.companies import Companies, company_schema, companies_schema
from lib.authenticate import authenticate, authenticate_return_auth
from util.reflection import populate_object


@authenticate_return_auth
def create_company(auth_info):
    if auth_info.user.role != "admin":
        return jsonify({"message": "not authorized"}), 403

    post_data = request.form if request.form else request.json
    new_company = Companies.new_company_obj()

    populate_object(new_company, post_data)

    db.session.add(new_company)
    db.session.commit()

    return jsonify({"message": "company created", "company": company_schema.dump(new_company)}), 201


@authenticate
def get_companies():
    companies = Companies.query.all()
    return jsonify({"companies": companies_schema.dump(companies)}), 200


@authenticate
def get_company_by_id(company_id):
    company = Companies.query.get(company_id)
    if not company:
        return jsonify({"message": "company not found"}), 404
    return jsonify({"company": company_schema.dump(company)}), 200


@authenticate_return_auth
def update_company(company_id, auth_info):
    if auth_info.user.role != "admin":
        return jsonify({"message": "not authorized"}), 403

    post_data = request.form if request.form else request.json
    company = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company:
        return jsonify({"message": "company not found"}), 404

    populate_object(company, post_data)
    db.session.commit()

    return jsonify({"message": "company updated", "company": company_schema.dump(company)}), 200


@authenticate_return_auth
def delete_company(company_id, auth_info):
    if auth_info.user.role != "admin":
        return jsonify({"message": "not authorized"}), 403

    company = Companies.query.get(company_id)
    if not company:
        return jsonify({"message": "company not found"}), 404

    db.session.delete(company)
    db.session.commit()

    return jsonify({"message": "company deleted"}), 200
