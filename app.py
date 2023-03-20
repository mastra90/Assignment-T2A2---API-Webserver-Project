from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Configuration
app = Flask(__name__)
connection = "postgresql+psycopg2://box_office_db_dev:963.@localhost:5432/box_office_db"

#Connection
app.config["SQLALCHEMY_DATABASE_URI"] = connection
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Models:
class Movies(db.Model):
    # tablename
    __tablename__ = "movies"
    # Primary key
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # additional attributes
    title = db.Column(db.String())
    genre = db.Column(db.String())
    year_released = db.Column(db.Integer)
    runtime = db.Column(db.Interval())
    rotten_tomatoes_rating = db.Column(db.Integer)

#SCHEMAS
class MoviesSchema(ma.Schema):
    class Meta:
        fields = ("movie_id", "title", "genre", "year_released", "runtime", "rotten_tomatoes_rating")

# Schema to handle many or all movies list
movies_schema = MoviesSchema(many=True)
# Schema to handle single movie
movie_schema = MoviesSchema()


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
@app.cli.command("seed")
def seed_movies_table():
    for add_movie in movies_dict:
        db.session.add(Movies(**add_movie))
    db.session.commit()
    print("Movies seeded successfully")

# List of movies
movies_dict = [
    {
        "title": "Avatar",
        "genre": "Fantasy",
        "year_released": 2009,
        "runtime": "2:42:00",
        "rotten_tomatoes_rating": 82
    },
    {
        "title": "Avengers: Endgame",
        "genre": "Action",
        "year_released": 2019,
        "runtime": "3:01:00",
        "rotten_tomatoes_rating": 94
    },
    {
        "title": "Avatar: The Way of Water",
        "genre": "Fantasy",
        "year_released": 2022,
        "runtime": "3:12:00",
        "rotten_tomatoes_rating": 76 
    },
    {
        "title": "Titanic",
        "genre": "Drama",
        "year_released": 1997,
        "runtime": "3:14:00",
        "rotten_tomatoes_rating": 88
    },
    {
        "title": "Star Wars: Episode VII - The Force Awakens",
        "genre": "Sci-Fi",
        "year_released": 2015,
        "runtime": "2:18:00",
        "rotten_tomatoes_rating": 93
    },
    {
        "title": "Avengers: Infinity War",
        "genre": "Action",
        "year_released": 2018,
        "runtime": "2:19:00",
        "rotten_tomatoes_rating": 85
    },
    {
        "title": "Spider-Man: No Way Home",
        "genre": "Action",
        "year_released": 2021,
        "runtime": "2:28:00",
        "rotten_tomatoes_rating": 93
    },
    {
        "title": "Jurassic World",
        "genre": "Sci-Fi",
        "year_released": 2015,
        "runtime": "2:4:00",
        "rotten_tomatoes_rating": 71
    },
    {
        "title": "The Lion King",
        "genre": "Adventure",
        "year_released": 2019,
        "runtime": "1:58:00",
        "rotten_tomatoes_rating": 52
    },
    {
        "title": "The Avengers",
        "genre": "Action",
        "year_released": 2012,
        "runtime": "2:23:00",
        "rotten_tomatoes_rating": 91
    }
    # Add more movies to the list:
    
    # {
    #     "title": "",
    #     "genre": "",
    #     "year_released": ,
    #     "runtime": "",
    #     "rotten_tomatoes_rating": 
    # },
    
]

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
    return jsonify(output)

# Displays a movie from movie_id
@app.route("/movies/<int:id>", methods=["GET"])
def get_specific_movie(id):
    movie = Movies.query.get(id) 
    # output = movie_schema.dump(movie)
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