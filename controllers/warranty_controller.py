from flask import request, jsonify
from db import db
from models.warranties import Warranties, warranty_schema, warranties_schema
from lib.authenticate import authenticate, require_role
from util.reflection import populate_object


@authenticate
@require_role("admin")
def create_warranty(auth_info):
    data = request.get_json() or request.form
    warranty_name = data.get("warranty_name")
    duration_months = data.get("duration_months")
    product_id = data.get("product_id")

    if not warranty_name or duration_months is None or not product_id:
        return jsonify({"message": "warranty_name, duration_months, and product_id are required"}), 400

    if Warranties.query.filter_by(warranty_name=warranty_name).first():
        return jsonify({"message": "warranty already exists"}), 400

    new_warranty = Warranties(
        warranty_name=warranty_name,
        duration_months=duration_months,
        product_id=product_id,
        description=data.get("description")
    )

    db.session.add(new_warranty)
    db.session.commit()

    return jsonify({"message": "warranty created", "warranty": warranty_schema.dump(new_warranty)}), 201



@authenticate
def get_warranties(auth_info):
    all_warranties = Warranties.query.all()
    return jsonify({"message": "warranties found", "warranties": warranties_schema.dump(all_warranties)}), 200


@authenticate
def get_warranty_by_id(warranty_id, auth_info):
    warranty = Warranties.query.get(warranty_id)
    if not warranty:
        return jsonify({"message": "warranty not found"}), 404
    return jsonify({"message": "warranty found", "warranty": warranty_schema.dump(warranty)}), 200


@authenticate
@require_role("admin")
def update_warranty(warranty_id, auth_info):
    warranty = Warranties.query.get(warranty_id)
    if not warranty:
        return jsonify({"message": "warranty not found"}), 404

    data = request.get_json() or request.form
    populate_object(warranty, data)
    db.session.commit()

    return jsonify({"message": "warranty updated", "warranty": warranty_schema.dump(warranty)}), 200


@authenticate
@require_role("admin")
def delete_warranty(warranty_id, auth_info):
    warranty = Warranties.query.get(warranty_id)
    if not warranty:
        return jsonify({"message": "warranty not found"}), 404

    db.session.delete(warranty)
    db.session.commit()
    return jsonify({"message": "warranty deleted"}), 200
