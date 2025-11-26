from flask import request, jsonify
from db import db
from models.product_category_xref import ProductCategoryXref
from models.products import Products
from models.categories import Categories
from lib.authenticate import authenticate, require_role

@authenticate
@require_role("admin")
def add_product_category(auth_info):
    data = request.get_json() or request.form
    product_id = data.get("product_id")
    category_id = data.get("category_id")

    if not product_id or not category_id:
        return jsonify({"message": "product_id and category_id are required"}), 400

    product = Products.query.get(product_id)
    category = Categories.query.get(category_id)

    if not product or not category:
        return jsonify({"message": "invalid product_id or category_id"}), 404

    existing_link = ProductCategoryXref.query.filter_by(product_id=product_id, category_id=category_id).first()
    if existing_link:
        return jsonify({"message": "link already exists"}), 400

    link = ProductCategoryXref(product_id=product_id, category_id=category_id)
    db.session.add(link)
    db.session.commit()

    return jsonify({"message": "product linked to category"}), 201

@authenticate
@require_role("admin")
def remove_product_category(auth_info):
    data = request.get_json() or request.form
    product_id = data.get("product_id")
    category_id = data.get("category_id")

    link = ProductCategoryXref.query.filter_by(product_id=product_id, category_id=category_id).first()
    if not link:
        return jsonify({"message": "link not found"}), 404

    db.session.delete(link)
    db.session.commit()
    return jsonify({"message": "product-category link removed"}), 200
