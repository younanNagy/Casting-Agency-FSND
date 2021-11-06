
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

data_base_user_name=os.environ['UserName']
data_base_user_password=os.environ['Password']
data_base_url=os.environ['URL']
data_base_name=os.environ['DataBaseName']
database_path="postgresql://{}:{}@{}/{}".format(data_base_user_name,data_base_user_password,data_base_url,data_base_name)
db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    # migrate = Migrate(app, db)

