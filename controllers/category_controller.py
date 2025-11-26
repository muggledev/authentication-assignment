from flask import request, jsonify
from db import db
from models.categories import Categories, category_schema, categories_schema
from lib.authenticate import authenticate, require_role
from util.reflection import populate_object

@authenticate
@require_role("admin")
def create_category(auth_info):
    data = request.get_json() or request.form
    category_name = data.get("category_name")
    if not category_name:
        return jsonify({"message": "category name is required"}), 400

    if Categories.query.filter_by(category_name=category_name).first():
        return jsonify({"message": "category already exists"}), 400

    new_category = Categories(category_name=category_name, description=data.get("description"))
    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "category created", "category": category_schema.dump(new_category)}), 201

@authenticate
def get_categories(auth_info):
    all_categories = Categories.query.all()
    return jsonify({"message": "categories found", "categories": categories_schema.dump(all_categories)}), 200

@authenticate
def get_category_by_id(category_id, auth_info):
    category = Categories.query.get(category_id)
    if not category:
        return jsonify({"message": "category not found"}), 404
    return jsonify({"message": "category found", "category": category_schema.dump(category)}), 200

@authenticate
@require_role("admin")
def update_category(category_id, auth_info):
    category = Categories.query.get(category_id)
    if not category:
        return jsonify({"message": "category not found"}), 404

    data = request.get_json() or request.form

    new_name = data.get("category_name")
    if new_name and Categories.query.filter(Categories.category_name == new_name, Categories.category_id != category_id).first():
        return jsonify({"message": "category name already exists"}), 400

    populate_object(category, data)
    db.session.commit()

    return jsonify({"message": "category updated", "category": category_schema.dump(category)}), 200

@authenticate
@require_role("admin")
def delete_category(category_id, auth_info):
    category = Categories.query.get(category_id)
    if not category:
        return jsonify({"message": "category not found"}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "category deleted"}), 200
