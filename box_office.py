def seed_box_office_table(BoxOffice, db):
    for add_box_office in box_office_dict:
        db.session.add(BoxOffice(**add_box_office))
    db.session.commit()
    print("BoxOffice seeded successfully")

# List of directors
box_office_dict = [
    {
        # Avatar
        "worldwide_gross": "2923706026",
        "domestic_gross": "106654050",
        "movie_id": 1
    },
    { 
        # Avengers: Endgame
        "worldwide_gross": "2799439100",
        "domestic_gross": "59113013",
        "movie_id": 2
    },
    {
        # Avatar: The Way of Water
        "worldwide_gross": "2304184543",
        "domestic_gross": "63058230",
        "movie_id": 3
    },
    {
        # Titanic
        "worldwide_gross": "2256092642",
        "domestic_gross": "38891987",
        "movie_id": 4
    },
    {
        # Star Wars: Episode VII - The Force Awakens
        "worldwide_gross": "2071310218",
        "domestic_gross": "72465422",
        "movie_id": 5
    },
    {
        # Avengers: Infinity War
        "worldwide_gross": "2052415039",
        "domestic_gross": "46825158",
        "movie_id": 6
    },
    {
        # Spider-Man: No Way Home
        "worldwide_gross": "1921847111",
        "domestic_gross": "54546201",
        "movie_id": 7
    },
    {
        # Jurassic World
        "worldwide_gross": "1671537444",
        "domestic_gross": "38978832	",
        "movie_id": 8
    },
    {
        # The Lion King
        "worldwide_gross": "1663075401",
        "domestic_gross": "45183380",
        "movie_id": 9
    },
    {
        # The Avengers
        "worldwide_gross": "1520538536",
        "domestic_gross": "54385465",
        "movie_id": 10
    }
]

