import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

from path_utils import data_file, output_file

# 1. Load training data
train_df = pd.read_excel(data_file("training_data.xlsx"))
train_df = train_df.dropna()

# 2. Define features and target
X = train_df[['Actuation_Score', 'Awareness_Score', 'Connectivity_Score',
              'Dynamism_Score', 'Novelty_Score', 'Personality_Score']]

y = train_df['predicted_sentiments'].astype(str)

# 3. Train model
model = RandomForestClassifier(
    random_state=42,
    n_estimators=300
)

model.fit(X, y)

print("Model training completed successfully.")

# 4. Save trained model
joblib.dump(model, output_file("model.pkl"))

print("Model saved as 'model.pkl' inside outputs folder.")
