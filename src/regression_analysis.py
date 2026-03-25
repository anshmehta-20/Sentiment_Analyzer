import pandas as pd
import statsmodels.api as sm

from path_utils import existing_output_file

matrix_df = pd.read_excel(existing_output_file("review_matrix.xlsx"))

constructs = ["Awareness", "Actuation", "Connectivity", "Dynamism", "Novelty", "Personality"]

X = matrix_df[constructs]
y = matrix_df["Rating"]

X = sm.add_constant(X)

model = sm.OLS(y, X).fit()

print(model.summary())
