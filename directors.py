def seed_directors_table(Director, db):
    for add_director in directors_dict:
        db.session.add(Director(**add_director))
    db.session.commit()
    print("Directors seeded successfully")

directors_dict = [
    {
        "name": "James Cameron",
        "age": 68,
        "movie_id": 1
    },
    {
        "name": "Anthony Russo",
        "age": 53,
        "movie_id": 2
    },
    # Add more directors to the list, with corresponding movie_id
]






