from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#establish connection
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:@localhost:5432/box_office_db"
db = SQLAlchemy(app)

class Movies(db.Model):
    # tablename
    __tablename__ = "movies"
    # Primary key
    movie_id = db.Column(db.Serial(), primary_key=True)
    # additional attributes
    title = db.Column(db.String())
    genre = db.Column(db.String())
    year_released = db.Column(db.Integer)
    runtime = db.Column(db.Interval())
    rotten_tomatoes_rating = db.Column(db.Integer)


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

