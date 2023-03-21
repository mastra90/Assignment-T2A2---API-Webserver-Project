from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movies(db.Model):
    # tablename
    __tablename__ = "movies"
    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # additional attributes
    title = db.Column(db.String(), nullable=False, unique=True)
    genre = db.Column(db.String())
    year_released = db.Column(db.Integer)
    runtime = db.Column(db.Interval())
    rotten_tomatoes_rating = db.Column(db.Integer)
    directors = db.relationship("Directors", backref="owner")

class Directors(db.Model):
    # tablename
    __tablename__ = "directors"
    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # additional attributes
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"))  