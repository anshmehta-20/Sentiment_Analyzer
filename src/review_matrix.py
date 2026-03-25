import pandas as pd

from path_utils import data_file, output_file

df = pd.read_excel(data_file("final_data.xlsx"))

df.columns = df.columns.str.strip().str.lower()
df = df.dropna(subset=["clean_review", "most_similar_characteristic", "sentiment"])

constructs = ["Awareness", "Actuation", "Connectivity", "Dynamism", "Novelty", "Personality"]

sentiment_map = {"positive": 1, "neutral": 0, "negative": -1}
df["sentiment_score"] = df["sentiment"].str.lower().map(sentiment_map)

matrix_data = []

for review, group in df.groupby("clean_review"):
    scores = {c: [] for c in constructs}

    for _, row in group.iterrows():
        construct = row["most_similar_characteristic"]
        sentiment = row["sentiment_score"]

        if pd.notna(construct):
            construct = construct.capitalize()
            if construct in scores:
                scores[construct].append(sentiment)

    avg_scores = {c: (sum(v) / len(v) if v else 0) for c, v in scores.items()}
    rating = group["rating"].iloc[0] if "rating" in group.columns else 0

    matrix_data.append([review] + [avg_scores[c] for c in constructs] + [rating])

matrix_df = pd.DataFrame(matrix_data, columns=["Review"] + constructs + ["Rating"])
matrix_df.fillna(0, inplace=True)

matrix_df.to_excel(output_file("review_matrix.xlsx"), index=False)

print("Review matrix created.")
