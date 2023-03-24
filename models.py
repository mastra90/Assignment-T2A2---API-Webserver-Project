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
    box_office_id = db.relationship("BoxOffice", backref="movies", uselist=False)
    lead_actor_id = db.relationship("LeadActor", backref="movies", uselist=False)
    

class Directors(db.Model):
    # tablename
    __tablename__ = "directors"
    # Primary key
    director_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # additional attributes
    name = db.Column(db.String(), nullable=False)
    dob = db.Column(db.String())
    movies = db.relationship("Movies", backref="director") 

class BoxOffice(db.Model):
    # tablename
    __tablename__ = "box_office"
    # Primary key
    box_office_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # additional attributes
    worldwide_gross = db.Column(db.Float, nullable=False)
    domestic_gross = db.Column(db.Float)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))

class LeadActor(db.Model):
    __tablename__ = "lead_actor"
    lead_actor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lead_actor_name = db.Column(db.String(), nullable=False)
    lead_character_name = db.Column(db.String(), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))


