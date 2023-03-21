def seed_directors_table(Directors, db):
    for add_director in directors_dict:
        db.session.add(Directors(**add_director))
    db.session.commit()
    print("Directors seeded successfully")

# List of directors
directors_dict = [
    {
        # Avatar
        "name": "James Cameron",
        "dob": "16/08/1954"
    },
    { 
        # Avengers: Endgame
        "name": "Anthony Russo",
        "dob": "03/02/1970"
    },
    {
        # Avatar: The Way of Water
        "name": "James Cameron",
        "dob": "16/08/1954"
    },
    {
        # Titanic
        "name": "James Cameron",
        "dob": "16/08/1954"
    },
    {
        # Star Wars: Episode VII - The Force Awakens
        "name": "J.J. Abrams",
        "dob": "27/03/1963"
    },
    {
        # Avengers: Infinity War
        "name": "Anthony Russo",
        "dob": "03/02/1970"
    },
    {
        # Spider-Man: No Way Home
        "name": "Jon Watts",
        "dob": "28/06/1981"
    },
    {
        # Jurassic World
        "name": "Colin Trevorrow",
        "dob": "13/09/1976"
    },
    {
        # The Lion King
        "name": "Jon Favreau",
        "dob": "19/10/1966"
    },
    {
        # The Avengers
        "name": "Joss Whedon",
        "dob": "23/06/1964"
    }
]
    # Add more directors to the list, with corresponding movie_id
