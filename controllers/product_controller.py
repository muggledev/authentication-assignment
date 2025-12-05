from flask import request, jsonify
from db import db
from models.products import Products, product_schema, products_schema
from models.categories import Categories
from models.companies import Companies
from lib.authenticate import authenticate, authenticate_return_auth
from util.reflection import populate_object


@authenticate_return_auth
def create_product(auth_info):
    if auth_info.user.role != "admin":
        return jsonify({"message": "not authorized"}), 403

    post_data = request.form if request.form else request.json
    new_product = Products.new_product_obj()

    populate_object(new_product, post_data)

    if "category_ids" in post_data:
        new_product.categories = []
        for cid in post_data["category_ids"]:
            cat = Categories.query.get(cid)
            if cat:
                new_product.categories.append(cat)

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "product created", "product": product_schema.dump(new_product)}), 201


@authenticate
def get_products():
    products = Products.query.all()
    return jsonify({"products": products_schema.dump(products)}), 200


@authenticate
def get_active_products():
    products = Products.query.filter_by(active=True).all()
    return jsonify({"products": products_schema.dump(products)}), 200


@authenticate
def get_product_by_id(product_id):
    product = Products.query.get(product_id)
    if not product:
        return jsonify({"message": "product not found"}), 404
    return jsonify({"product": product_schema.dump(product)}), 200


@authenticate
def get_products_by_company(company_id):
    company = Companies.query.get(company_id)
    if not company:
        return jsonify({"message": "company not found"}), 404

    products = Products.query.filter_by(company_id=company_id).all()
    return jsonify({"products": products_schema.dump(products)}), 200


@authenticate_return_auth
def update_product(product_id, auth_info):
    if auth_info.user.role != "admin":
        return jsonify({"message": "not authorized"}), 403

    post_data = request.form if request.form else request.json
    product = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product:
        return jsonify({"message": "product not found"}), 404

    populate_object(product, post_data)

    if "category_ids" in post_data:
        product.categories = []
        for cid in post_data["category_ids"]:
            category = Categories.query.get(cid)
            if category:
                product.categories.append(category)

    db.session.commit()

    return jsonify({"message": "product updated", "product": product_schema.dump(product)}), 200


@authenticate_return_auth
def delete_product(product_id, auth_info):
    if auth_info.user.role != "admin":
        return jsonify({"message": "not authorized"}), 403

    product = Products.query.get(product_id)
    if not product:
        return jsonify({"message": "product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "product deleted"}), 200
    return jsonify({"message": "product deleted"}), 200
