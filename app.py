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

