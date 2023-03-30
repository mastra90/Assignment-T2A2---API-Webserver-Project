from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from movies import seed_movies_table
from directors import seed_directors_table
from models import db, Movies, Directors, BoxOffice, LeadActor
from box_office import seed_box_office_table
from lead_actor import seed_lead_actor_table
from marshmallow import post_dump


# App configuration
app = Flask(__name__)
connection = "postgresql+psycopg2://box_office_db_dev:963.@localhost:5432/box_office_db"

#Connection to db
app.config["SQLALCHEMY_DATABASE_URI"] = connection
db.init_app(app)
ma = Marshmallow(app)

# ***********************SCHEMAS************************



# Convert the runtime field to HH:MM:SS in Flask (otherwise the server displays the runtime in raw seconds)
def seconds_to_hhmmss(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

# --------Movie Schema--------
class MoviesSchema(ma.Schema):
    class Meta:
        fields = ("movie_id", "title", "genre", "year_released", "runtime", "rotten_tomatoes_rating", "director_id")
    
    # Flush to execute the seconds_to_hhmmss function 
    @post_dump(pass_many=True)
    def format_runtime(self, data, many):
        if many:
            for item in data:
                item["runtime"] = seconds_to_hhmmss(item["runtime"])
        else:
            data["runtime"] = seconds_to_hhmmss(data["runtime"])
        return data

# Schema to handle many or all movies
movies_schema = MoviesSchema(many=True)
# Schema to handle a single movie
movie_schema = MoviesSchema()


# --------Director Schema--------
class DirectorsSchema(ma.Schema):
    class Meta:
        fields = ("director_id", "name", "dob")
# Schema to handle many or all directors
directors_schema = DirectorsSchema(many=True)
# Schema to handle a single director
director_schema = DirectorsSchema()


# -------Box office Schema-------
class BoxOfficeSchema(ma.Schema):
    class Meta:
        fields = ("box_office_id", "worldwide_gross", "domestic_gross", "movie_id")
# Schema to handle many or all box office entires
box_offices_schema = BoxOfficeSchema(many=True)
# Schema to handle a single box office entry
box_office_schema = BoxOfficeSchema()


# -------Lead actor Schema-------
class LeadActorSchema(ma.Schema):
    class Meta:
        fields = ("lead_actor_id", "lead_actor_name", "lead_character_name", "movie_id")
# Schema to handle all lead actors
lead_actors_schema = LeadActorSchema(many=True)
# Schema to handle a single lead actor
lead_actor_schema = LeadActorSchema()



# ***********************CLI commands***********************

# Function to create all tables
@app.cli.command("create")
def create_db():
    db.create_all()
    print ("Tables created successfully")

# Function to delete all tables
@app.cli.command("drop")
def create_db():
    db.drop_all()
    print ("Tables dropped successfully")

# Function to seed all tables
@app.cli.command("seed_all")
def seed_all_tables():
    seed_directors()
    seed_movies()
    seed_box_office()
    seed_lead_actor ()

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

# Function to seed the box_office table
@app.cli.command("seed_box_office")
def seed_box_office_cli():
    seed_box_office()

def seed_box_office():
    from app import BoxOffice, db
    seed_box_office_table(BoxOffice, db)

# Function to seed the lead_actor table
@app.cli.command("seed_lead_actor")
def seed_lead_actor_cli():
    seed_lead_actor()

def seed_lead_actor():
    from app import LeadActor, db
    seed_lead_actor_table(LeadActor, db)


# ******************** GET ********************

# Homepage
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
                <a href="/tables/movies" style="color: #F5F6ED; font-size: 20px;">View All Movies</a>
                <a href="/tables/directors" style="color: #F5F6ED; font-size: 20px;">View All Directors</a>
                <a href="/tables/box_office" style="color: #F5F6ED; font-size: 20px;">View Box office earnings</a>
                <a href="/tables/lead_actors" style="color: #F5F6ED; font-size: 20px;">View Lead actors</a>
            </div>
        </body>
    </html>
    """

# Displays all tables
@app.route("/all", methods=["GET"])
def get_all_data():
    # Fetch data from each table
    movies_list = Movies.query.all()
    directors_list = Directors.query.all()
    box_offices_list = BoxOffice.query.all()
    lead_actors_list = LeadActor.query.all()

    # Serialize data using schemas
    movies_output = movies_schema.dump(movies_list)
    directors_output = directors_schema.dump(directors_list)
    box_offices_output = box_offices_schema.dump(box_offices_list)
    lead_actors_output = lead_actors_schema.dump(lead_actors_list)

    # Store the serialized data in a dictionary
    output = {
        "movies": movies_output,
        "directors": directors_output,
        "box_office": box_offices_output,
        "lead_actors": lead_actors_output
    }

    # Return the dictionary as the response
    return output, 200

@app.route("/all/<int:movie_id>", methods=["GET"])
def get_specific_movie_id_all_tables(movie_id):
    # Find the movie by id
    movie = Movies.query.get(movie_id)
    if movie is None:
        return {"ERROR": "Movie not found."}, 404

    # Fetch related data using the relationships between tables
    director = movie.director
    box_office = movie.box_office_id
    lead_actor = movie.lead_actor_id

    # Serialize data using the schemas
    movie_output = movie_schema.dump(movie)
    director_output = director_schema.dump(director)
    box_office_output = box_office_schema.dump(box_office)
    lead_actor_output = lead_actor_schema.dump(lead_actor)

    # Store the serialized data in a dictionary
    output = {
        "movie": movie_output,
        "director": director_output,
        "box_office": box_office_output,
        "lead_actor": lead_actor_output
    }

    return output, 200


@app.route("/all/<string:movie_title>", methods=["GET"])
def get_specific_movie_title_all_tables(movie_title):
    # Find the movie by title
    movie = Movies.query.filter_by(title=movie_title).first()
    if movie is None:
        return {"ERROR": "Movie not found. Please note that the movie search is cap sensitive."}, 404

    # Fetch related data using the relationships between tables
    director = movie.director
    box_office = movie.box_office_id
    lead_actor = movie.lead_actor_id

    # Serialize data using the corresponding schemas
    movie_output = movie_schema.dump(movie)
    director_output = director_schema.dump(director)
    box_office_output = box_office_schema.dump(box_office)
    lead_actor_output = lead_actor_schema.dump(lead_actor)

    # Store the serialized data in a dictionary
    output = {
        "movie": movie_output,
        "director": director_output,
        "box_office": box_office_output,
        "lead_actor": lead_actor_output
    }

    return output, 200


# Displays entire movies table
@app.route("/tables/movies", methods=["GET"])
def get_all_movies():
    movies_list = Movies.query.all() 
    output = movies_schema.dump(movies_list)
    return (output), 200


# Displays a single movie from movie_id
@app.route("/tables/movies/<int:movie_title>", methods=["GET"])
def get_specific_movie(movie_title):
    movie = Movies.query.get(movie_title) 
    if movie is None:
        return {"ERROR": "Movie not found"}, 404
    return movie_schema.dump(movie), 200

# Displays entire directors table
@app.route("/tables/directors", methods=["GET"])
def get_all_directors():
    directors_list = Directors.query.all() 
    output = directors_schema.dump(directors_list)
    return (output), 200

# Displays a single director from director_id
@app.route("/tables/directors/<int:director_id>", methods=["GET"])
def get_specific_director(director_id):
    director = Directors.query.get(director_id) 
    if director is None:
        return {"ERROR": "Director not found."}, 404
    return director_schema.dump(director), 200


# Displays entire box_office table
@app.route("/tables/box_office", methods=["GET"])
def get_all_box_offices():
    box_offices_list = BoxOffice.query.all() 
    output = box_offices_schema.dump(box_offices_list)
    return (output), 200

# Displays a single box_office entry from box_office_id
@app.route("/tables/box_office/<int:box_office_id>", methods=["GET"])
def get_specific_box_office(box_office_id):
    box_office = BoxOffice.query.get(box_office_id) 
    if box_office is None:
        return {"ERROR": "Box office value not found."}, 404
    return box_office_schema.dump(box_office) ,200


# Displays entire lead actors table
@app.route("/tables/lead_actors", methods=["GET"])
def get_all_lead_actors():
    lead_actors_list = LeadActor.query.all() 
    output = lead_actors_schema.dump(lead_actors_list)
    return (output), 200

# Displays a single lead actor from lead_actor_id
@app.route("/tables/lead_actors/<int:lead_actor_id>", methods=["GET"])
def get_specific_lead_actor(lead_actor_id):
    lead_actor = LeadActor.query.get(lead_actor_id) 
    if lead_actor is None:
        return {"ERROR": "Lead actor not found."}, 404
    return lead_actor_schema.dump(lead_actor) ,200

# ******************** POST ********************

@app.route("/post_movie", methods=["POST"])
def post_movie():
    # Extract the JSON data from the request
    json_data = request.get_json()

    # Separate the JSON data into the different sections (director, movie, box office, lead actor)
    director_data = json_data[0]
    movie_data = json_data[1]
    box_office_data = json_data[2]
    lead_actor_data = json_data[3]

    # Validates the data using schemas
    director_fields = director_schema.load(director_data)
    movie_fields = movie_schema.load(movie_data)
    box_office_fields = box_office_schema.load(box_office_data)
    lead_actor_fields = lead_actor_schema.load(lead_actor_data)

    # Extract the necessary ids and movie title for validation checks
    director_id = movie_fields["director_id"]
    movie_id_box = box_office_fields["movie_id"]
    movie_id_actor = lead_actor_fields["movie_id"]
    movie_title = movie_fields["title"]

    # Check if the provided movie title already exists in the movies table
    existing_movie_title = Movies.query.filter_by(title=movie_title).first()
    if existing_movie_title:
        return jsonify({"ERROR": "The provided movie title is already in the database. Please provide a unique movie title."}), 405

    # Check if the provided movie_id already exists in the box_office table
    existing_movie = Movies.query.filter_by(movie_id=movie_id_box).first()
    if existing_movie:
        return jsonify({"ERROR": "The provided movie_id is already in use. Please provide a unique movie_id."}), 405
    
    # Check if the provided movie_id already exists in the lead_actor table
    existing_movie = Movies.query.filter_by(movie_id=movie_id_actor).first()
    if existing_movie:
        return jsonify({"ERROR": "The provided movie_id is already in use. Please provide a unique movie_id."}), 405

    # Check if the provided director_id already exists in the directors table
    existing_director = Directors.query.filter_by(director_id=director_id).first()
    if existing_director:
        return jsonify({"ERROR": "The provided director_id is already in use. Please provide a unique director_id."}), 405

    # Create new instances of the Director, Movie, BoxOffice, and LeadActor models
    director = Directors(
        name=director_fields["name"],
        dob=director_fields["dob"])

    movie = Movies(
        title=movie_fields["title"],
        genre=movie_fields["genre"],
        year_released=movie_fields["year_released"],
        runtime=movie_fields["runtime"],
        rotten_tomatoes_rating=movie_fields["rotten_tomatoes_rating"],
        director_id=movie_fields["director_id"])

    box_office = BoxOffice(
        worldwide_gross=box_office_fields["worldwide_gross"],
        domestic_gross=box_office_fields["domestic_gross"],
        movie_id=box_office_fields["movie_id"])

    lead_actor = LeadActor(
        lead_actor_name=lead_actor_fields["lead_actor_name"],
        lead_character_name=lead_actor_fields["lead_character_name"],
        movie_id=lead_actor_fields["movie_id"])

    # Add the new instances to the database session and commit the changes
    db.session.add_all([director, movie, box_office, lead_actor])
    db.session.commit()
    return jsonify(Success=movie.title + " has been added", 
                movie=movie_schema.dump(movie),
                director=director_schema.dump(director),
                box_office=box_office_schema.dump(box_office),
                lead_actor=lead_actor_schema.dump(lead_actor)), 200


# ******************* DELETE *******************

@app.route("/delete_movie/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    # Store the query in the "movie" variable
    movie = Movies.query.get(movie_id)
    if not movie:
        return jsonify({"ERROR": "Movie not found."}), 404
    else:
        db.session.delete(movie)
        db.session.commit()
        return jsonify({"Success": "Movie deleted successfully."}), 200

    
# ******************* UPDATE *******************
    

@app.route("/movies/update_rt/<int:movie_id>", methods=["PUT"])
def update_movie(movie_id):
    movie = Movies.query.get(movie_id)

    if not movie:
        return jsonify({"ERROR": "Movie not found"}), 404
    movie_fields = movie_schema.load(request.json)
    # Only the rotten_tomatoes_rating column is allowed to be updated
    movie.rotten_tomatoes_rating = movie_fields.get("rotten_tomatoes_rating", movie.rotten_tomatoes_rating)
    db.session.commit()
    return jsonify(Success="Rotten Tomatoes rating updated.", movie=movie_schema.dump(movie)), 200


@app.route("/box_office/update_bo/<int:box_office_id>", methods=["PUT"])
def update_box_office(box_office_id):
    box_office = BoxOffice.query.get(box_office_id)

    if not box_office:
        return jsonify({"ERROR": "Box office entry not found."}), 404
    
    box_office_fields = box_office_schema.load(request.json)
    # Each line is what fields are possible to update
    box_office.worldwide_gross = box_office_fields.get("worldwide_gross", box_office.worldwide_gross)
    box_office.domestic_gross = box_office_fields.get("domestic_gross", box_office.domestic_gross)

    db.session.commit()
    return jsonify(Success="Box office entry updated.", box_office=box_office_schema.dump(box_office)), 200
