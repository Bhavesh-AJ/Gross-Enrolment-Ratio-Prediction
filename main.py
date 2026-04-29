import numpy as np
import pandas as pd

from extract_2018 import get_2018_data
from extract_2019 import get_2019_data
from extract_2020 import get_2020_data
from extract_2021 import get_2021_data

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import KFold, cross_val_predict, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


file_2018 = "data/AISHE FINAL REPORT 2018-17.xlsx"
file_2019 = "data/AISHE Final Report 2019-20.xlsx"
file_2020 = "data/AISHE Final Report 2020-21.xlsx"
file_2021 = "data/AISHE Final Report 2021-22.xlsx"


df_final = pd.concat([
    get_2018_data(file_2018),
    get_2019_data(file_2019),
    get_2020_data(file_2020),
    get_2021_data(file_2021),
], ignore_index=True)

df_final = df_final.dropna()
df_final = df_final[(df_final["ger"] > 5) & (df_final["ger"] < 80)]

df_final["students_per_uni"] = df_final["students"] / df_final["universities"]
df_final["faculty_per_student"] = df_final["faculty"] / df_final["students"]
df_final["enrollment_rate_proxy"] = (df_final["students"] / df_final["population_18_23"]) * 100
df_final["universities_per_lakh_population"] = (
    df_final["universities"] / df_final["population_18_23"]
) * 100000
df_final["faculty_per_lakh_population"] = (
    df_final["faculty"] / df_final["population_18_23"]
) * 100000

df_final.replace([np.inf, -np.inf], np.nan, inplace=True)
df_final = df_final.dropna()

feature_sets = {
    "Definition-aware model": [
        "enrollment_rate_proxy",
        "students_per_uni",
        "faculty_per_student",
        "universities_per_lakh_population",
        "faculty_per_lakh_population",
    ],
    "Infrastructure-only model": [
        "students_per_uni",
        "faculty_per_student",
        "universities_per_lakh_population",
        "faculty_per_lakh_population",
        "year",
    ],
}

y = df_final["ger"]

print("Final Dataset Shape:", df_final.shape)
print("Rows by year:")
print(df_final["year"].value_counts().sort_index())

models = {
    "Linear Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LinearRegression()),
    ]),
    "Ridge Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", Ridge(alpha=1.0)),
    ]),
    "Polynomial Ridge Regression": Pipeline([
        ("poly", PolynomialFeatures(degree=2, include_bias=False)),
        ("scaler", StandardScaler()),
        ("model", Ridge(alpha=0.001)),
    ]),
}

for set_name, features in feature_sets.items():
    X = df_final[features]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"\n=== {set_name} ===")
    print("\n--- HOLDOUT PERFORMANCE ---")
    best_name = None
    best_model = None
    best_mae = float("inf")

    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, pred)
        r2 = r2_score(y_test, pred)
        mape = np.nanmean(np.abs((y_test - pred) / y_test.replace(0, np.nan))) * 100

        print(f"\n{name}")
        print("MAE:", round(mae, 3))
        print("R2:", round(r2, 3))
        print("MAPE:", round(mape, 2))

        if mae < best_mae:
            best_name = name
            best_model = model
            best_mae = mae

    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_pred = cross_val_predict(best_model, X, y, cv=cv)

    print(f"\n--- 5-FOLD CV PERFORMANCE ({best_name}) ---")
    print("MAE:", round(mean_absolute_error(y, cv_pred), 3))
    print("R2:", round(r2_score(y, cv_pred), 3))
    print("MAPE:", round(np.nanmean(np.abs((y - cv_pred) / y.replace(0, np.nan))) * 100, 2))

    best_model.fit(X, y)
    linear_model = best_model.named_steps["model"]
    if hasattr(linear_model, "coef_"):
        coefficient_names = features
        if "poly" in best_model.named_steps:
            coefficient_names = best_model.named_steps["poly"].get_feature_names_out(features)

        print("\nFeature Coefficients:")
        print(pd.Series(linear_model.coef_, index=coefficient_names).sort_values(ascending=False).head(10))

df_final.to_csv("final_dataset.csv", index=False)
