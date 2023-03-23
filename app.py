from flask import Flask, request
from flask_marshmallow import Marshmallow
from movies import seed_movies_table
from directors import seed_directors_table
from models import db, Movies, Directors, BoxOffice
from box_office import seed_box_office_table



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

class BoxOfficeSchema(ma.Schema):
    class Meta:
        fields = ("box_office_id", "worldwide_gross", "domestic_gross", "movie_id")
# Schema to handle many or all box_offices
box_offices_schema = BoxOfficeSchema(many=True)
# Schema to handle single box_office
box_office_schema = BoxOfficeSchema()


# CLI commands:
@app.cli.command("create")
def create_db():
    db.create_all()
    print ("Tables created successfully")

@app.cli.command("drop")
def create_db():
    db.drop_all()
    print ("Tables dropped successfully")

@app.cli.command("seed_all")
def seed_all_tables():
    seed_directors()
    seed_movies()
    seed_box_office()

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

@app.cli.command("seed_box_office")
def seed_box_office_cli():
    seed_box_office()

def seed_box_office():
    from app import BoxOffice, db
    seed_box_office_table(BoxOffice, db)


# Routes

@app.route("/")
def index():
    return """
    <html>
        <head>
            <title>Welcome to Movie DB</title>
        </head>
        <body style="background-color: #121212;">
            <h1 style="color: #F5F6ED; text-align: center;">Welcome to Movie DB</h1>
            <div style="text-align: center;">
                <a href="/movies" style="color: #F5F6ED; font-size: 20px;">View All Movies</a>
                <a href="/directors" style="color: #F5F6ED; font-size: 20px;">View All Directors</a>
                <a href="/box_office" style="color: #F5F6ED; font-size: 20px;">View Box_office</a>
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
            <body style="background-color: #121212;">
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
            <body style="background-color: #121212;">
                <h1 style="color: #F5F6ED; text-align: center;">Director not found!</h1>
                <div style="text-align: center;"></div>
            </body>
        </html>
        """
    return director_schema.dump(director)


# Displays all box_offices
@app.route("/box_office", methods=["GET"])
def get_all_box_offices():
    box_offices_list = BoxOffice.query.all() 
    # con holds converted to format that works from schema
    output = box_offices_schema.dump(box_offices_list)
    return (output)

# Displays a box_office entry from box_office_id
@app.route("/box_office/<int:id>", methods=["GET"])
def get_specific_box_office(id):
    box_office = BoxOffice.query.get(id) 
    if box_office is None:
        return """
        <html>
            <head>
                <title>Box Office entry not found!</title>
            </head>
            <body style="background-color: #121212;">
                <h1 style="color: #F5F6ED; text-align: center;">Box Office entry not found!</h1>
                <div style="text-align: center;"></div>
            </body>
        </html>
        """
    return box_office_schema.dump(box_office)





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

