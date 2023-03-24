def seed_lead_actor_table(LeadActor, db):
    for add_lead_character in lead_character_dict:
        db.session.add(LeadActor(**add_lead_character))
    db.session.commit()
    print("BoxOffice seeded successfully")

# List of directors
lead_character_dict = [
    {
        # Avatar
        "lead_actor_name": "Sam Worthington",
        "lead_character_name": "Jake Sully",
        "movie_id": 1
    },
    { 
        # Avengers: Endgame
        "lead_actor_name": "Robert Downey Jr.",
        "lead_character_name": "Tony Stark/Iron Man",
        "movie_id": 2
    },
    {
        # Avatar: The Way of Water
        "lead_actor_name": "Sam Worthington",
        "lead_character_name": "Jake Sully",
        "movie_id": 3
    },
    {
        # Titanic
        "lead_actor_name": "Leonardo DiCaprio",
        "lead_character_name": "Jack Dawson",
        "movie_id": 4
    },
    {
        # Star Wars: Episode VII - The Force Awakens
        "lead_actor_name": "Daisy Ridley",
        "lead_character_name": "Rey Skywalker",
        "movie_id": 5
    },
    {
        # Avengers: Infinity War
        "lead_actor_name": "Robert Downey Jr.",
        "lead_character_name": "Tony Stark/Iron Man",
        "movie_id": 6
    },
    {
        # Spider-Man: No Way Home
        "lead_actor_name": "Tom Holland",
        "lead_character_name": "Peter Parker/Spider-Man",
        "movie_id": 7
    },
    {
        # Jurassic World
        "lead_actor_name": "Chris Pratt",
        "lead_character_name": "Owen Grady",
        "movie_id": 8
    },
    {
        # The Lion King
        "lead_actor_name": "Donald Glover",
        "lead_character_name": "Simba",
        "movie_id": 9
    },
    {
        # The Avengers
        "lead_actor_name": "Robert Downey Jr.",
        "lead_character_name": "Tony Stark/Iron Man",
        "movie_id": 10
    }
]
