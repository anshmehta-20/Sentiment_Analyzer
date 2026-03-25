import pandas as pd
import joblib

from path_utils import data_file, existing_output_file, output_file

# Load model
model = joblib.load(existing_output_file("model.pkl"), mmap_mode="r")

# Load testing data
test_df = pd.read_excel(data_file("testing_data.xlsx")).dropna()

X = test_df[['Actuation_Score', 'Awareness_Score', 'Connectivity_Score',
             'Dynamism_Score', 'Novelty_Score', 'Personality_Score']]

# Predict
y_pred = model.predict(X)

test_df['Predicted_Sentiment_Output'] = y_pred
test_df.to_excel(output_file("testing_results.xlsx"), index=False)

print("Testing predictions saved.")

# New predictions
predict_df = pd.read_excel(data_file("prediction_data.xlsx"))

X_new = predict_df[['Actuation_Score', 'Awareness_Score', 'Connectivity_Score',
                    'Dynamism_Score', 'Novelty_Score', 'Personality_Score']]

y_new = model.predict(X_new)

predict_df['Predicted_Sentiment_Output'] = y_new
predict_df.to_excel(output_file("prediction_results.xlsx"), index=False)

print("New predictions saved.")
