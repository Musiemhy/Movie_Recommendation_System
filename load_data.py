from neo4j import GraphDatabase
import pandas as pd

def connect_to_neo4j(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver

def load_data_to_neo4j(driver, users_file, movies_file, ratings_file):
    users_df = pd.read_csv(users_file)
    movies_df = pd.read_csv(movies_file)
    ratings_df = pd.read_csv(ratings_file)

    with driver.session() as session:
        for _, row in users_df.iterrows():
            session.run(
                """
                MERGE (u:User {id: $id})
                SET u.name = $name, u.age = $age, u.location = $location
                """,
                id=row["userId"], name=row["name"], age=row["age"], location=row["location"]
            )
            print(f"Loaded user: {row['userId']}")

        for _, row in movies_df.iterrows():
            if isinstance(row["genres"], str):
                genres = row["genres"].split(', ')
            else:
                genres = [None]

            session.run(
                """
                MERGE (m:Movie {id: $id})
                SET m.title = $title, m.release_year = $release_year, m.rating = $rating
                """,
                id=row["movieId"], title=row["title"], release_year=row["release_year"],
                rating=row["rating"]
            )
            print(f"Loaded movie: {row['movieId']}")

            for genre in genres:
                if genre: 
                    session.run(
                        """
                        MATCH (m:Movie {id: $movieId})
                        MERGE (g:Genre {name: $genre})
                        MERGE (m)-[:BELONGS_TO]->(g)
                        """,
                        movieId=row["movieId"], genre=genre
                    )
                    print(f"Associated movie: {row['movieId']} with genre: {genre}")

        for _, row in ratings_df.iterrows():
            session.run(
                """
                MATCH (u:User {id: $userId})
                MATCH (m:Movie {id: $movieId})
                MERGE (u)-[r:WATCHED]->(m)
                SET r.rating = $rating
                """,
                userId=row["userId"], movieId=row["movieId"], rating=row["rating"]
            )
            print(f"Loaded rating for user: {row['userId']} on movie: {row['movieId']}")

if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "password"
    driver = connect_to_neo4j(uri, user, password)

    users_file = "data/fake_users.csv"
    movies_file = "data/cleaned_movies_metadata.csv"
    ratings_file = "data/ratings_small.csv"

    load_data_to_neo4j(driver, users_file, movies_file, ratings_file)

    driver.close()
