def seed_movies_table(Movies, db):
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
        "rotten_tomatoes_rating": 82,
        "director_id": 1
    },
    {
        "title": "Avengers: Endgame",
        "genre": "Action",
        "year_released": 2019,
        "runtime": "3:01:00",
        "rotten_tomatoes_rating": 94,
        "director_id": 2
    },
    {
        "title": "Avatar: The Way of Water",
        "genre": "Fantasy",
        "year_released": 2022,
        "runtime": "3:12:00",
        "rotten_tomatoes_rating": 76,
        "director_id": 3
    },
    {
        "title": "Titanic",
        "genre": "Drama",
        "year_released": 1997,
        "runtime": "3:14:00",
        "rotten_tomatoes_rating": 88,
        "director_id": 4
    },
    {
        "title": "Star Wars: Episode VII - The Force Awakens",
        "genre": "Sci-Fi",
        "year_released": 2015,
        "runtime": "2:18:00",
        "rotten_tomatoes_rating": 93,
        "director_id": 5
    },
    {
        "title": "Avengers: Infinity War",
        "genre": "Action",
        "year_released": 2018,
        "runtime": "2:19:00",
        "rotten_tomatoes_rating": 85,
        "director_id": 6
    },
    {
        "title": "Spider-Man: No Way Home",
        "genre": "Action",
        "year_released": 2021,
        "runtime": "2:28:00",
        "rotten_tomatoes_rating": 93,
        "director_id": 7
    },
    {
        "title": "Jurassic World",
        "genre": "Sci-Fi",
        "year_released": 2015,
        "runtime": "2:4:00",
        "rotten_tomatoes_rating": 71,
        "director_id": 8
    },
    {
        "title": "The Lion King",
        "genre": "Adventure",
        "year_released": 2019,
        "runtime": "1:58:00",
        "rotten_tomatoes_rating": 52,
        "director_id": 9
    },
    {
        "title": "The Avengers",
        "genre": "Action",
        "year_released": 2012,
        "runtime": "2:23:00",
        "rotten_tomatoes_rating": 91,
        "director_id": 10
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