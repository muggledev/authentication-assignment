from flask import request, jsonify
from db import db
from models.products import Products, product_schema, products_schema
from models.categories import Categories
from models.companies import Companies
from lib.authenticate import authenticate, require_role
from util.reflection import populate_object

@authenticate
@require_role("admin")
def create_product(auth_info):
    data = request.get_json() or request.form

    product_name = data.get("product_name")
    company_id = data.get("company_id")

    if not product_name or not company_id:
        return jsonify({"message": "product name and company_id required"}), 400

    company = Companies.query.get(company_id)
    if not company:
        return jsonify({"message": "company not found"}), 404

    new_product = Products(
        product_name=product_name,
        description=data.get("description"),
        price=data.get("price", 0),
        company_id=company_id,
        active=data.get("active", True)
    )

    category_ids = data.get("category_ids", [])
    for cid in category_ids:
        cat = Categories.query.get(cid)
        if cat:
            new_product.categories.append(cat)

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "product created", "product": product_schema.dump(new_product)}), 201

@authenticate
def get_products(auth_info):
    all_products = Products.query.all()
    return jsonify({"message": "products found", "products": products_schema.dump(all_products)}), 200

@authenticate
def get_active_products(auth_info):
    active_products = Products.query.filter_by(active=True).all()
    return jsonify({
        "message": f"{len(active_products)} active products found",
        "products": products_schema.dump(active_products)
    }), 200

@authenticate
def get_product_by_id(product_id, auth_info):
    product = Products.query.get(product_id)
    if not product:
        return jsonify({"message": "product not found"}), 404
    return jsonify({"message": "product found", "product": product_schema.dump(product)}), 200

@authenticate
def get_products_by_company(company_id, auth_info):
    company = Companies.query.get(company_id)
    if not company:
        return jsonify({"message": "company not found"}), 404

    products = Products.query.filter_by(company_id=company_id).all()
    return jsonify({
        "message": f"{len(products)} products found for company",
        "products": products_schema.dump(products)
    }), 200

@authenticate
@require_role("admin")
def update_product(product_id, auth_info):
    product = Products.query.get(product_id)
    if not product:
        return jsonify({"message": "product not found"}), 404

    data = request.get_json() or request.form
    populate_object(product, data)

    if "category_ids" in data:
        product.categories = []
        for cid in data["category_ids"]:
            cat = Categories.query.get(cid)
            if cat:
                product.categories.append(cat)

    db.session.commit()
    return jsonify({"message": "product updated", "product": product_schema.dump(product)}), 200

@authenticate
@require_role("admin")
def delete_product(product_id, auth_info):
    product = Products.query.get(product_id)
    if not product:
        return jsonify({"message": "product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "product deleted"}), 200
