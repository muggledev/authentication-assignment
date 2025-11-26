from flask import request, jsonify
from db import db
from models.companies import Companies, company_schema, companies_schema
from lib.authenticate import authenticate, require_role
from util.reflection import populate_object


@authenticate
@require_role("admin")
def create_company(auth_info):
    data = request.get_json() or request.form
    company_name = data.get("company_name")

    if not company_name:
        return jsonify({"message": "company name is required"}), 400

    if Companies.query.filter_by(company_name=company_name).first():
        return jsonify({"message": "company already exists"}), 400

    new_company = Companies(company_name=company_name)
    populate_object(new_company, data)

    db.session.add(new_company)
    db.session.commit()

    return jsonify({"message": "company created", "company": company_schema.dump(new_company)}), 201


@authenticate
def get_companies(auth_info):
    all_companies = Companies.query.all()
    return jsonify({"message": "companies found", "companies": companies_schema.dump(all_companies)}), 200


@authenticate
def get_company_by_id(company_id, auth_info):
    company = Companies.query.get(company_id)
    if not company:
        return jsonify({"message": "company not found"}), 404
    return jsonify({"message": "company found", "company": company_schema.dump(company)}), 200


@authenticate
@require_role("admin")
def update_company(company_id, auth_info):
    company = Companies.query.get(company_id)
    if not company:
        return jsonify({"message": "company not found"}), 404

    data = request.get_json() or request.form

    new_name = data.get("company_name")
    if new_name and Companies.query.filter(Companies.company_name == new_name, Companies.company_id != company_id).first():
        return jsonify({"message": "company name already exists"}), 400

    populate_object(company, data)

    db.session.commit()
    return jsonify({"message": "company updated", "company": company_schema.dump(company)}), 200


@authenticate
@require_role("admin")
def delete_company(company_id, auth_info):
    company = Companies.query.get(company_id)
    if not company:
        return jsonify({"message": "company not found"}), 404

    db.session.delete(company)
    db.session.commit()
    return jsonify({"message": "company deleted"}), 200
