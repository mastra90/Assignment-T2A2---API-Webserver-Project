from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movies(db.Model):
    # tablename
    __tablename__ = "movies"
    # Primary key
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # additional attributes
    title = db.Column(db.String(), nullable=False, unique=True)
    genre = db.Column(db.String())
    year_released = db.Column(db.Integer)
    runtime = db.Column(db.Interval())
    rotten_tomatoes_rating = db.Column(db.Integer)
    director_id = db.Column(db.Integer, db.ForeignKey("directors.director_id"))

class Directors(db.Model):
    # tablename
    __tablename__ = "directors"
    # Primary key
    director_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # additional attributes
    name = db.Column(db.String(), nullable=False)
    dob = db.Column(db.String())
    movies = db.relationship("Movies", backref="director") 