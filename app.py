from flask import Flask, request
from flask_marshmallow import Marshmallow
from movies import seed_movies_table
from directors import seed_directors_table
from models import db, Movies, Directors


# Configuration
app = Flask(__name__)
connection = "postgresql+psycopg2://box_office_db_dev:963.@localhost:5432/box_office_db"

#Connection
app.config["SQLALCHEMY_DATABASE_URI"] = connection
db.init_app(app)
ma = Marshmallow(app)

#SCHEMAS

# Movie (goes to server)
class MoviesSchema(ma.Schema):
    class Meta:
        fields = ("movie_id", "title", "genre", "year_released", "runtime", "rotten_tomatoes_rating", "director_id")

# Schema to handle many or all movies
movies_schema = MoviesSchema(many=True)
# Schema to handle single movie
movie_schema = MoviesSchema()

# Director Schema

class DirectorsSchema(ma.Schema):
    class Meta:
        fields = ("director_id", "name", "dob")
# Schema to handle many or all directors
directors_schema = DirectorsSchema(many=True)
# Schema to handle single director
director_schema = DirectorsSchema()


# CLI commands:
@app.cli.command("create")
def create_db():
    db.create_all()
    print ("Tables created successfully")

@app.cli.command("drop")
def create_db():
    db.drop_all()
    print ("Tables dropped successfully")

# Function to seed the movies table
@app.cli.command("seed_movies")
def seed_movies_cli():
    seed_movies()
    
def seed_movies():
    from app import Movies, db
    seed_movies_table(Movies, db)

# Function to seed the directors table
@app.cli.command("seed_directors")
def seed_directors_cli():
    seed_directors()

def seed_directors():
    from app import Directors, db
    seed_directors_table(Directors, db)


# Routes

@app.route("/")
def index():
    return """
    <html>
        <head>
            <title>Welcome to Movie DB</title>
        </head>
        <body style="background-color: #131410;">
            <h1 style="color: #F5F6ED; text-align: center;">Welcome to Movie DB</h1>
            <div style="text-align: center;">
                <a href="/movies" style="color: #F5F6ED; font-size: 20px;">View All Movies</a>
                <a href="/directors" style="color: #F5F6ED; font-size: 20px;">View All Directors</a>
            </div>
        </body>
    </html>
    """


# Displays all movies
@app.route("/movies", methods=["GET"])
def get_all_movies():
    movies_list = Movies.query.all() 
    # con holds converted to format that works from schema
    output = movies_schema.dump(movies_list)
    return (output)


# Displays a movie from movie_id
@app.route("/movies/<int:id>", methods=["GET"])
def get_specific_movie(id):
    movie = Movies.query.get(id) 
    if movie is None:
        return """
        <html>
            <head>
                <title>Movie not found!</title>
            </head>
            <body style="background-color: #131410;">
                <h1 style="color: #F5F6ED; text-align: center;">Movie not found!</h1>
                <div style="text-align: center;"></div>
            </body>
        </html>
        """
    return movie_schema.dump(movie)

# Displays all directors
@app.route("/directors", methods=["GET"])
def get_all_directors():
    directors_list = Directors.query.all() 
    # con holds converted to format that works from schema
    output = directors_schema.dump(directors_list)
    return (output)

# Displays a director from director_id
@app.route("/directors/<int:id>", methods=["GET"])
def get_specific_director(id):
    director = Directors.query.get(id) 
    if director is None:
        return """
        <html>
            <head>
                <title>Director not found!</title>
            </head>
            <body style="background-color: #131410;">
                <h1 style="color: #F5F6ED; text-align: center;">Director not found!</h1>
                <div style="text-align: center;"></div>
            </body>
        </html>
        """
    return director_schema.dump(director)







@app.route("/movies", methods=["POST"])
def post_movie():
    movie_fields = movie_schema.load(request.json)

    movie = Movies (
        title = movie_fields["title"],
        genre = movie_fields["genre"],
        year_released = movie_fields["year_released"],
        runtime = movie_fields["runtime"],
        rotten_tomatoes_rating = movie_fields["rotten_tomatoes_rating"])
    db.session.add(movie)
    db.session.commit()
    print (movie.title + " has been added")
    return movie_schema.dump(movie)