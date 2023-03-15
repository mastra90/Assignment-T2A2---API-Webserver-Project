from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configuration
app = Flask(__name__)
connection = "postgresql+psycopg2://box_office_db_dev:963.@localhost:5432/box_office_db"

#Connection
app.config["SQLALCHEMY_DATABASE_URI"] = connection
db = SQLAlchemy(app)

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

# CLI commands:
@app.cli.command("create")
def create_db():
    db.create_all()
    print ("Tables created")

@app.cli.command("drop")
def create_db():
    db.drop_all()
    print ("Tables dropped")

# List of movies
movies_list = [
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
    # Add more movies to the list
    # {
    #     "title": "",
    #     "genre": "",
    #     "year_released": ,
    #     "runtime": "",
    #     "rotten_tomatoes_rating": 
    # },
    
]

# Function to seed the movies table
@app.cli.command("seed")
def seed_movies_table():
    for add_movie in movies_list:
        db.session.add(Movies(**add_movie))
    db.session.commit()
    print("Movies seeded successfully")

# Routes

@app.route("/")
def index():
    return """
    <html>
        <head>
            <title>Welcome to Movie DB test</title>
        </head>
        <body style="background-color: #131410;">
            <h1 style="color: #F5F6ED; text-align: center;">Welcome to Movie DB</h1>
        </body>
    </html>
    """

