from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app, database):
    database.init_app(app)
