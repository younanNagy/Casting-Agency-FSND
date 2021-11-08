
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# data_base_user_name=os.environ['UserName']
# data_base_user_password=os.environ['Password']
# data_base_url=os.environ['URL']
# data_base_name=os.environ['DataBaseName']
# database_path="postgresql://{}:{}@{}/{}".format(data_base_user_name,data_base_user_password,data_base_url,data_base_name)
database_path = 'postgresql://postgres:2271996@localhost:5432/castingagency'
db = SQLAlchemy()


def setupDB(app,database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    
    

def createAll():
    db.create_all()

def setupMigration(app):
    migrate = Migrate(app, db)
    
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    release_date = db.Column(db.Date(), nullable=False)
    genre = db.Column(db.String(), nullable=False, default='')
    # actors = db.relationship('Actor', secondary=actor_movie_relationship_table,
    #                          backref=db.backref('movie', lazy=True))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return({
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date.isoformat(),
            "genre": self.genre
        })

    def __repr__(self):
        return f'Movie:{self.id}, {self.title}'




class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return({
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        })

    def __repr__(self):
        return f'Actor: {self.id}, {self.name}'


