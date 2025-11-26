import routes

def register_blueprints(app):
    app.register_blueprint(routes.auth_tokens)
    app.register_blueprint(routes.categories)
    app.register_blueprint(routes.companies)
    app.register_blueprint(routes.products)
    app.register_blueprint(routes.users)
    app.register_blueprint(routes.warranties)
    app.register_blueprint(routes.product_category_xref)
