from flask import request, jsonify
from db import db
from models.warranties import Warranties, warranty_schema, warranties_schema
from lib.authenticate import authenticate, authenticate_return_auth
from util.reflection import populate_object


@authenticate_return_auth
def create_warranty(auth_info):
    if auth_info.user.role != "admin":
        return jsonify({"message": "not authorized"}), 403

    post_data = request.form if request.form else request.json
    new_warranty = Warranties.new_warranty_obj()

    populate_object(new_warranty, post_data)

    db.session.add(new_warranty)
    db.session.commit()

    return jsonify({"message": "warranty created", "warranty": warranty_schema.dump(new_warranty)}), 201


@authenticate
def get_warranties():
    warranties = Warranties.query.all()
    return jsonify({"warranties": warranties_schema.dump(warranties)}), 200


@authenticate
def get_warranty_by_id(warranty_id):
    warranty = Warranties.query.get(warranty_id)
    if not warranty:
        return jsonify({"message": "warranty not found"}), 404
    return jsonify({"warranty": warranty_schema.dump(warranty)}), 200


@authenticate_return_auth
def update_warranty(warranty_id, auth_info):
    if auth_info.user.role != "admin":
        return jsonify({"message": "not authorized"}), 403

    post_data = request.form if request.form else request.json
    warranty = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty:
        return jsonify({"message": "warranty not found"}), 404

    populate_object(warranty, post_data)
    db.session.commit()

    return jsonify({"message": "warranty updated", "warranty": warranty_schema.dump(warranty)}), 200


@authenticate_return_auth
def delete_warranty(warranty_id, auth_info):
    if auth_info.user.role != "admin":
        return jsonify({"message": "not authorized"}), 403

    warranty = Warranties.query.get(warranty_id)
    if not warranty:
        return jsonify({"message": "warranty not found"}), 404

    db.session.delete(warranty)
    db.session.commit()

    return jsonify({"message": "warranty deleted"}), 200
