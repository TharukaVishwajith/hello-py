import os

from flask import Flask
from app.sqla import sqla

import pymysql


from app import post

from app import db


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    db.init_app(app)

    from app import secrets

    # configure SQLAlchemy
    # app.config.from_mapping(SQLALCHEMY_DATABASE_URI=f'sqlite:///{app.config["DATABASE"]}',
    #                         SQLALCHEMY_TRACK_MODIFICATIONS=False)
    conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(
        secrets.dbuser, secrets.dbpassword, secrets.dbhost, secrets.dbname)
    app.config.from_mapping(SQLALCHEMY_DATABASE_URI=conn,
                            SQLALCHEMY_TRACK_MODIFICATIONS=False)
    sqla.init_app(app)

    app.register_blueprint(post.bp, url_prefix="/post")

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app
