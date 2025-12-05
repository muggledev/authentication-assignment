from flask import request, jsonify
from db import db
from models.categories import Categories, category_schema, categories_schema
from lib.authenticate import authenticate, authenticate_return_auth
from util.reflection import populate_object


@authenticate_return_auth
def create_category(auth_info):
    if auth_info.user.role != "admin":
        return jsonify({"message": "not authorized"}), 403

    post_data = request.form if request.form else request.json
    new_category = Categories.new_category_obj()

    populate_object(new_category, post_data)

    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "category created", "category": category_schema.dump(new_category)}), 201


@authenticate
def get_categories():
    categories = Categories.query.all()
    return jsonify({"categories": categories_schema.dump(categories)}), 200


@authenticate
def get_category_by_id(category_id):
    category = Categories.query.get(category_id)
    if not category:
        return jsonify({"message": "category not found"}), 404
    return jsonify({"category": category_schema.dump(category)}), 200


@authenticate_return_auth
def update_category(category_id, auth_info):
    if auth_info.user.role != "admin":
        return jsonify({"message": "not authorized"}), 403

    post_data = request.form if request.form else request.json
    category = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category:
        return jsonify({"message": "category not found"}), 404

    populate_object(category, post_data)
    db.session.commit()

    return jsonify({"message": "category updated", "category": category_schema.dump(category)}), 200


@authenticate_return_auth
def delete_category(category_id, auth_info):
    if auth_info.user.role != "admin":
        return jsonify({"message": "not authorized"}), 403

    category = Categories.query.get(category_id)
    if not category:
        return jsonify({"message": "category not found"}), 404

    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "category deleted"}), 200
