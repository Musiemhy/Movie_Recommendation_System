# Movie_Recommendation_System

a movie recommendation system for a training task at iCog-Labs using python and Neo4j. It incorporates both content-based and collaborative filtering techniques to recommend movies to users.

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repository/movie-recommendation-system.git
   cd movie-recommendation-system
   ```
2. **Install Dependencies:**

   ```bash
   Copy code
   pip install -r requirements.txt
   ```

3. **Set Up Neo4j:**
   Install Neo4j and start the server.
   Set the uri, user, and password values in load_data.py and recommend.py to match your Neo4j setup.
   Prepare the Data:

   Ensure the data files are placed in the data/ directory:
   fake_users.csv
   cleaned_movies_metadata.csv
   ratings_small.csv

4. **Load Data into Neo4j:**

   ```bash
   Copy code
   python load_data.py
   ```

5. **Run the Recommendation System:**

   ```bash
   Copy code
   python recommend.py
   ```
