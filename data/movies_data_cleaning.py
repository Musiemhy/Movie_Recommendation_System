import pandas as pd
import ast

original_file = "movies_metadata.csv"
output_file = "cleaned_movies_metadata.csv"

df = pd.read_csv(original_file, low_memory=False)

columns_to_keep = ["id", "title", "genres", "release_date", "vote_average"]
df_cleaned = df[columns_to_keep]

df_cleaned = df_cleaned[df_cleaned["genres"].notna() & (df_cleaned["genres"].str.strip() != "")]

def parse_genres(genre_str):
    try:
        genres = ast.literal_eval(genre_str)
        if isinstance(genres, list) and genres: 
            return ", ".join([genre["name"] for genre in genres])
        return None 
    except (ValueError, SyntaxError): 
        return None

df_cleaned["genres"] = df_cleaned["genres"].apply(parse_genres)

df_cleaned = df_cleaned[df_cleaned["genres"].notna() & (df_cleaned["genres"].str.strip() != "")]

df_cleaned["release_year"] = pd.to_datetime(df_cleaned["release_date"], errors="coerce").dt.year

df_cleaned.rename(columns={"vote_average": "rating"}, inplace=True)

df_cleaned.rename(columns={"id": "movieId"}, inplace=True)

df_cleaned.dropna(subset=["movieId", "title", "genres", "release_year", "rating"], inplace=True)

df_cleaned.to_csv(output_file, index=False, encoding="utf-8")

print(f"Cleaned dataset saved to {output_file}")
