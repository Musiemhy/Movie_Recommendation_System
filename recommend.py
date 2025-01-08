from neo4j import GraphDatabase

def connect_to_neo4j(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver

def collaborative_filtering(driver, user_id):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (u1:User)-[r:WATCHED]->(m:Movie)<-[r2:WATCHED]-(u2:User)
            WHERE u1.id = $user_id AND r.rating >= 4
            MATCH (u2)-[:WATCHED]->(rec:Movie)
            WHERE NOT EXISTS {
                MATCH (u1)-[:WATCHED]->(rec)
            }
            RETURN DISTINCT rec.title AS recommendation, rec.rating AS avg_rating
            ORDER BY avg_rating DESC
            LIMIT 5
            """,
            user_id=user_id,
        )
        return result.data()

def content_based_filtering(driver, user_id):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (u:User {id: $user_id})-[:WATCHED]->(m:Movie)-[:BELONGS_TO]->(g:Genre)<-[:BELONGS_TO]-(rec:Movie)
            WHERE NOT EXISTS {
                MATCH (u)-[:WATCHED]->(rec)
            }
            RETURN DISTINCT rec.title AS recommendation, rec.rating AS avg_rating
            ORDER BY avg_rating DESC
            LIMIT 5
            """,
            user_id=user_id,
        )
        return result.data()

def recommend_movies(driver, user_id):
    recommendations = collaborative_filtering(driver, user_id)

    if not recommendations:
        print("No collaborative recommendations found. Falling back to content-based filtering.")
        recommendations = content_based_filtering(driver, user_id)

    return recommendations

if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "password"
    driver = connect_to_neo4j(uri, user, password)

    user_id = int(input("Please enter the user ID for recommendations: "))

    recommendations = recommend_movies(driver, user_id)

    print("Recommended Movies:")
    if recommendations:
        for rec in recommendations:
            print(f"Title: {rec['recommendation']}, Average Rating: {rec['avg_rating']}")
    else:
        print("No recommendations available.")
    
    driver.close()
