# Smart Sentiment Analyzer

Smart Sentiment Analyzer is a construct-based sentiment classification project. Instead of predicting sentiment directly from raw text, it uses six engineered "smartness construct" scores as model features:

- Actuation
- Awareness
- Connectivity
- Dynamism
- Novelty
- Personality

The project was originally developed using reviews of smartwatches, so the construct vocabulary and examples are grounded in that review domain.

## Use Case

This project was first applied to smartwatch reviews to study how users describe device smartness through constructs such as awareness, connectivity, dynamism, and personality. While the pipeline can be adapted to other product-review or text-analysis settings, the current seed words and examples are most naturally aligned with smartwatch-related language.

The project includes scripts for:

- generating construct scores from raw text with a seed-word scorer
- training a sentiment model
- generating predictions for new records
- building a review-level construct matrix
- running regression analysis against ratings

## Raw Text Support

This repository now includes a basic preprocessing script that can score arbitrary text using a seed-word approach:

- `src/construct_scoring.py`

It can read a CSV or Excel file, inspect a text column, and generate:

- `Actuation_Score`
- `Awareness_Score`
- `Connectivity_Score`
- `Dynamism_Score`
- `Novelty_Score`
- `Personality_Score`
- `most_similar_characteristic`

This makes the project usable on general text inputs, but it is still a lightweight lexical scorer rather than a full semantic NLP pipeline. The quality of the scores depends on the seed words you choose.

## Project Structure

```text
Sentiment_Analyzer/
|-- src/
|   |-- construct_scoring.py
|   |-- model_training.py
|   |-- prediction.py
|   |-- review_matrix.py
|   |-- regression_analysis.py
|   |-- path_utils.py
|-- data/
|-- outputs/
|-- requirements.txt
|-- README.md
```

## Requirements

- Python 3.10+
- pip

Install dependencies:

```bash
pip install -r requirements.txt
```

## Expected Input Files

Datasets are intentionally not included in this repository. Place your own CSV or Excel files in the `data/` folder before running the scripts.

## Generate Construct Scores From Text

If you start with raw text, create the construct-score columns first:

```bash
python src/construct_scoring.py --input data/raw_reviews.xlsx --text-column review_text
```

By default, this writes a scored file to:

```text
outputs/raw_reviews_scored.xlsx
```

You can also choose a custom output path:

```bash
python src/construct_scoring.py --input data/raw_reviews.csv --text-column review_text --output data/prediction_data.xlsx
```

The generated file includes the original text plus:

- `Actuation_Score`
- `Awareness_Score`
- `Connectivity_Score`
- `Dynamism_Score`
- `Novelty_Score`
- `Personality_Score`
- `most_similar_characteristic`

## How The Scores Are Calculated

Each construct has a small seed-word list. The script:

1. normalizes the text to lowercase
2. counts keyword matches for each construct
3. divides the total matches by token count
4. stores the normalized value as that construct's score
5. assigns the construct with the highest raw match count as `most_similar_characteristic`

Example seed words used by the scorer:

- `Actuation`: autonomous, triggering, executing, responding, scheduling
- `Awareness`: sensing, detecting, monitoring, scanning, tracking
- `Connectivity`: synchronizing, pairing, linking, networking, communicating
- `Dynamism`: learning, adapting, updating, optimizing, personalizing
- `Novelty`: innovative, unique, stylish, original, creative
- `Personality`: expressive, playful, conversational, empathetic, relatable

### Data

Files: `data/training_data.xlsx`, `data/testing_data.xlsx`, `data/prediction_data.xlsx`

Required columns:

- `Actuation_Score`
- `Awareness_Score`
- `Connectivity_Score`
- `Dynamism_Score`
- `Novelty_Score`
- `Personality_Score`
- `predicted_sentiments`

### Review matrix data

File: `data/final_data.xlsx`

Required columns:

- `clean_review`
- `most_similar_characteristic`
- `sentiment`

Optional column:

- `rating`

`most_similar_characteristic` should map to one of the six constructs, and `sentiment` should contain values such as `positive`, `neutral`, or `negative`.

## How to Run

### Train the model

```bash
python src/model_training.py
```

Output:

- `outputs/model.pkl`

### Run predictions

```bash
python src/prediction.py
```

Outputs:

- `outputs/testing_results.xlsx`
- `outputs/prediction_results.xlsx`

### Build the review matrix

```bash
python src/review_matrix.py
```

Output:

- `outputs/review_matrix.xlsx`

### Run regression analysis

```bash
python src/regression_analysis.py
```

This script reads `outputs/review_matrix.xlsx` and prints the OLS regression summary to the terminal.

## Current Status

- `construct_scoring.py` can generate construct features from raw text files.
- `model_training.py` runs successfully.
- `prediction.py` runs successfully.
- `review_matrix.py` requires your own `data/final_data.xlsx`.
- `regression_analysis.py` requires `outputs/review_matrix.xlsx`, which is generated by `review_matrix.py`.

## Notes

- Generated outputs and local datasets are ignored by Git so the repository stays lightweight.
- The trained model can become very large depending on your dataset and hyperparameters.
- The raw-text scorer is rule-based, so you can improve results by tuning the seed words for your domain.
